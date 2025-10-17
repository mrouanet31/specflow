#!/usr/bin/env python3
"""
Simple CSV -> GitHub Issues importer.

Usage:
  GITHUB_TOKEN must be set in env.
  python scripts/github_issue_importer.py --repo owner/repo /path/to/backlog.csv [--dry-run] [--skip-existing]

CSV expected columns: title, body, estimate, labels, assignee

Features:
- dry-run (no API calls)
- skip-existing (skip creating if issue with same title exists)
- basic rate-limit/backoff handling
"""
import csv
import os
import sys
import time
import argparse
import requests
import concurrent.futures
from threading import Lock
from typing import Optional


GITHUB_API = "https://api.github.com"


def read_csv(path):
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = [r for r in reader]
    return rows


def get_headers(token):
    return {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github+json'
    }


def issue_exists(session, repo, title):
    # search issues in repo with exact title (simple, uses issues search endpoint)
    q = f'repo:{repo} "{title}" in:title'
    url = f'{GITHUB_API}/search/issues'
    params = {'q': q}
    r = session.get(url, params=params)
    if r.status_code != 200:
        raise RuntimeError(f'GitHub search failed: {r.status_code} {r.text}')
    data = r.json()
    for item in data.get('items', []):
        if item.get('title', '').strip() == title.strip():
            return True
    return False


def ensure_label(session, repo, label_name, color='ededed', description=''):
    # Try get label, otherwise create it
    url = f'{GITHUB_API}/repos/{repo}/labels/{label_name}'
    r = session.get(url)
    if r.status_code == 200:
        return True
    # create label
    create_url = f'{GITHUB_API}/repos/{repo}/labels'
    payload = {'name': label_name, 'color': color.lstrip('#'), 'description': description}
    r2 = session.post(create_url, json=payload)
    return r2.status_code in (200, 201)


def ensure_milestone(session, repo, milestone_title):
    # find existing milestone
    url = f'{GITHUB_API}/repos/{repo}/milestones'
    r = session.get(url, params={'state': 'all'})
    if r.status_code == 200:
        for m in r.json():
            if m.get('title') == milestone_title:
                return m.get('number')
    # create milestone
    create_url = f'{GITHUB_API}/repos/{repo}/milestones'
    r2 = session.post(create_url, json={'title': milestone_title})
    if r2.status_code in (200, 201):
        return r2.json().get('number')
    return None


def create_issue(session, repo, title, body, labels=None, assignee=None, milestone: Optional[int] = None, verbose: bool = False):
    url = f'{GITHUB_API}/repos/{repo}/issues'
    payload = {'title': title, 'body': body}
    if labels:
        labels_list = [l.strip() for l in labels.replace(';', ',').split(',') if l.strip()]
        payload['labels'] = labels_list
    if assignee:
        payload['assignees'] = [assignee]
    if milestone:
        payload['milestone'] = milestone
    if verbose:
        print('  -> POST', url, 'payload keys:', list(payload.keys()))
    r = session.post(url, json=payload)
    return r


def worker_task(args, row, index, results, lock):
    # create a separate session per worker
    token = os.getenv('GITHUB_TOKEN')
    session = requests.Session()
    if token:
        session.headers.update(get_headers(token))

    repo = args.repo
    verbose = args.verbose

    title = row.get('title') or row.get('Title') or ''
    body = row.get('body') or row.get('Body') or ''
    estimate = row.get('estimate') or ''
    labels = row.get('labels') or ''
    assignee = row.get('assignee') or row.get('Assignee') or ''
    milestone_cell = row.get('milestone') or row.get('Milestone') or ''

    if not title:
        with lock:
            results.append({'title': title, 'status': 'skipped', 'issue_url': '', 'error': 'missing title'})
        return

    full_body = body
    if estimate:
        full_body = f'Estimate: {estimate}\n\n' + full_body

    try:
        if args.skip_existing and not args.dry_run:
            try:
                if issue_exists(session, repo, title):
                    if verbose:
                        print(f'[{index}] Issue exists, skipping: {title}')
                    with lock:
                        results.append({'title': title, 'status': 'exists', 'issue_url': '', 'error': ''})
                    return
            except Exception as e:
                print(f'  -> Warning: could not check existing issues: {e}')

        # prepare labels
        if args.label_estimate and estimate:
            est_label = f'estimate:{estimate}'
            if labels:
                labels = labels + ',' + est_label
            else:
                labels = est_label

        if args.create_labels and labels and not args.dry_run:
            for lbl in [l.strip() for l in labels.replace(';', ',').split(',') if l.strip()]:
                try:
                    ensure_label(session, repo, lbl)
                except Exception as e:
                    print(f'  -> Warning creating label {lbl}: {e}')

        # milestone per-row or global
        milestone_number = None
        if milestone_cell:
            if not args.dry_run:
                milestone_number = ensure_milestone(session, repo, milestone_cell)
        elif args.milestone and not args.dry_run:
            milestone_number = ensure_milestone(session, repo, args.milestone)

        # parse assignees (comma-separated)
        if getattr(args, 'skip_assignees', False):
            assignees_list = []
        else:
            assignees_list = [a.strip() for a in assignee.split(',') if a.strip()]

        if args.dry_run:
            if verbose:
                print(f'[{index}] Dry run: would create issue: {title} labels={labels} assignees={assignees_list} milestone={milestone_cell or args.milestone}')
            with lock:
                results.append({'title': title, 'status': 'dry-run', 'issue_url': '', 'error': ''})
            return

        # create with retries
        retries = 3
        backoff = 1.0
        for attempt in range(1, retries + 1):
            try:
                # create
                url = f'{GITHUB_API}/repos/{repo}/issues'
                payload = {'title': title, 'body': full_body}
                if labels:
                    payload['labels'] = [l.strip() for l in labels.replace(';', ',').split(',') if l.strip()]
                if assignees_list:
                    payload['assignees'] = assignees_list
                if milestone_number:
                    payload['milestone'] = milestone_number

                if verbose:
                    print(f'[{index}] POST issue payload keys: {list(payload.keys())}')

                r = session.post(url, json=payload)
                if r.status_code == 201:
                    issue_url = r.json().get('html_url')
                    with lock:
                        results.append({'title': title, 'status': 'created', 'issue_url': issue_url, 'error': ''})
                    if verbose:
                        print(f'[{index}] Created: {issue_url}')
                    break
                elif r.status_code in (429, 502, 503, 504):
                    print(f'[{index}] Temporary error {r.status_code}, attempt {attempt}/{retries}, retrying after {backoff}s')
                    time.sleep(backoff)
                    backoff *= 2
                    continue
                else:
                    err = f'{r.status_code} {r.text}'
                    print(f'[{index}] Failed to create: {err}')
                    with lock:
                        results.append({'title': title, 'status': 'failed', 'issue_url': '', 'error': err})
                    break
            except requests.RequestException as e:
                print(f'[{index}] Request error: {e}, attempt {attempt}/{retries}')
                time.sleep(backoff)
                backoff *= 2
                continue

    except Exception as e:
        with lock:
            results.append({'title': title, 'status': 'failed', 'issue_url': '', 'error': str(e)})


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('repo', help='GitHub repo in format owner/repo')
    parser.add_argument('csv', help='Path to backlog CSV')
    parser.add_argument('--dry-run', action='store_true', help='Do not create issues, only print')
    parser.add_argument('--skip-existing', action='store_true', help='Skip creating issues if title exists')
    parser.add_argument('--sleep', type=float, default=0.5, help='Sleep between requests to avoid rate limits')
    parser.add_argument('--create-labels', action='store_true', help='Create labels if missing')
    parser.add_argument('--milestone', type=str, default=None, help='Assign issues to this milestone (create if missing)')
    parser.add_argument('--label-estimate', action='store_true', help='Create a label for the estimate (e.g. estimate:5)')
    parser.add_argument('--verbose', action='store_true', help='Verbose logging')
    parser.add_argument('--concurrency', type=int, default=1, help='Number of concurrent workers (default 1)')
    parser.add_argument('--skip-assignees', action='store_true', help='Do not set assignees from CSV')
    parser.add_argument('--output-file', type=str, default='import-results.csv', help='CSV output file for results')
    args = parser.parse_args()

    token = os.getenv('GITHUB_TOKEN')
    if not token and not args.dry_run:
        print('Error: GITHUB_TOKEN env var not set (required unless --dry-run).')
        sys.exit(1)

    rows = read_csv(args.csv)
    print(f'Read {len(rows)} rows from {args.csv}')

    session = requests.Session()
    if token:
        session.headers.update(get_headers(token))

    created = 0
    skipped = 0

    # prepare milestone if requested
    milestone_number = None
    token = os.getenv('GITHUB_TOKEN')
    if not token and not args.dry_run:
        print('Error: GITHUB_TOKEN env var not set (required unless --dry-run).')
        sys.exit(1)

    rows = read_csv(args.csv)
    print(f'Read {len(rows)} rows from {args.csv}')

    results = []
    lock = Lock()

    if args.concurrency <= 1:
        for i, row in enumerate(rows, start=1):
            print(f'Processing row {i}/{len(rows)}')
            worker_task(args, row, i, results, lock)
            time.sleep(args.sleep)
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.concurrency) as ex:
            futures = []
            for i, row in enumerate(rows, start=1):
                futures.append(ex.submit(worker_task, args, row, i, results, lock))
            # wait
            for f in concurrent.futures.as_completed(futures):
                pass

    # write results CSV
    out_path = args.output_file
    with open(out_path, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['title', 'status', 'issue_url', 'error']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in results:
            writer.writerow(r)

    print(f'Done. Results written to {out_path}')

if __name__ == '__main__':
    main()
