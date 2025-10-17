import csv
import os
import sys
from types import SimpleNamespace
from threading import Lock

import pytest

# Ensure project root is on sys.path so we can import the scripts package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from scripts.github_issue_importer import read_csv, worker_task


def make_args(**overrides):
    defaults = {
        'repo': 'owner/repo',
        'dry_run': True,
        'skip_existing': False,
        'sleep': 0.0,
        'create_labels': False,
        'milestone': None,
        'label_estimate': False,
        'verbose': False,
        'concurrency': 1,
        'output_file': 'import-results.csv',
    }
    defaults.update(overrides)
    return SimpleNamespace(**defaults)


def test_read_csv_reads_rows(tmp_path):
    p = tmp_path / "test.csv"
    data = [
        {'title': 'T1', 'body': 'B1', 'estimate': '3', 'labels': 'bug,high', 'assignee': 'alice'},
        {'title': 'T2', 'body': 'B2', 'estimate': '', 'labels': '', 'assignee': ''},
    ]
    with open(p, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(data[0].keys()))
        writer.writeheader()
        for r in data:
            writer.writerow(r)

    rows = read_csv(str(p))
    assert len(rows) == 2
    assert rows[0]['title'] == 'T1'
    assert rows[1]['body'] == 'B2'


def test_worker_task_dry_run_multiple_assignees_and_label_separators():
    args = make_args()
    row = {
        'title': 'Multi Assignees',
        'body': 'Testing',
        'estimate': '5',
        'labels': 'bug;urgent',
        'assignee': 'alice,bob',
        'milestone': '',
    }
    results = []
    lock = Lock()
    # should not raise and should append a dry-run result
    worker_task(args, row, 1, results, lock)
    assert len(results) == 1
    assert results[0]['status'] == 'dry-run'
    assert results[0]['title'] == 'Multi Assignees'


def test_worker_task_missing_title_skips():
    args = make_args()
    row = {'title': '', 'body': 'No title'}
    results = []
    lock = Lock()
    worker_task(args, row, 1, results, lock)
    assert len(results) == 1
    assert results[0]['status'] == 'skipped'
    assert 'missing title' in results[0]['error']
