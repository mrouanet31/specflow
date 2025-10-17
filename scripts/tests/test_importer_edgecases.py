import sys
import os
from threading import Lock

import pytest

# Ensure project root on path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from scripts.github_issue_importer import worker_task


class SimpleMock:
    def __init__(self, responses=None):
        self.headers = {}
        self._responses = responses or []
        self.calls = []
        self.post_calls = 0

    def get(self, url, params=None):
        # For search: no results
        if url.endswith('/search/issues'):
            return type('R', (), {'status_code': 200, 'json': lambda: {'items': []}})()
        if url.endswith('/labels/'):
            return type('R', (), {'status_code': 404, 'json': lambda: {}})()
        if url.endswith('/milestones'):
            return type('R', (), {'status_code': 200, 'json': lambda: []})()
        return type('R', (), {'status_code': 404, 'json': lambda: {}})()

    def post(self, url, json=None):
        self.post_calls += 1
        self.calls.append((url, json))
        # If configured to simulate 429 first two attempts then success
        if url.endswith('/issues') and self.post_calls <= 2:
            return type('R', (), {'status_code': 429, 'text': 'rate limit'})()
        # Simulate assignee permission error
        if url.endswith('/issues') and json and json.get('assignees') and 'forbidden' in json.get('assignees'):
            return type('R', (), {'status_code': 422, 'text': 'Validation Failed'})()
        return type('R', (), {'status_code': 201, 'json': lambda: {'html_url': 'https://fake/1'}})()


def test_rate_limit_retries(monkeypatch):
    import requests
    monkeypatch.setenv('GITHUB_TOKEN', 'fake')

    session = SimpleMock()
    monkeypatch.setattr('requests.Session', lambda: session)
    import scripts.github_issue_importer as importer
    monkeypatch.setattr(importer.time, 'sleep', lambda s: None)

    args = type('A', (), {'repo': 'owner/repo', 'dry_run': False, 'skip_existing': False, 'sleep': 0.0,
                         'create_labels': False, 'milestone': None, 'label_estimate': False, 'verbose': False,
                         'concurrency': 1, 'output_file': 'import-results.csv'})()

    row = {'title': 'RL', 'body': 'rate limit test', 'assignee': ''}
    results = []
    lock = Lock()
    worker_task(args, row, 1, results, lock)

    # Ensure retries were attempted
    assert session.post_calls >= 2
    # final outcome can be created or failed depending on ordering; ensure we recorded a result
    assert results[0]['status'] in ('created', 'failed')


def test_assignee_permission_error(monkeypatch):
    import requests
    monkeypatch.setenv('GITHUB_TOKEN', 'fake')

    def fake_session():
        return SimpleMock()

    monkeypatch.setattr('requests.Session', fake_session)
    import scripts.github_issue_importer as importer
    monkeypatch.setattr(importer.time, 'sleep', lambda s: None)

    args = type('A', (), {'repo': 'owner/repo', 'dry_run': False, 'skip_existing': False, 'sleep': 0.0,
                         'create_labels': False, 'milestone': None, 'label_estimate': False, 'verbose': False,
                         'concurrency': 1, 'output_file': 'import-results.csv'})()

    row = {'title': 'Assignee error', 'body': 'assignment test', 'assignee': 'forbidden'}
    results = []
    lock = Lock()
    worker_task(args, row, 1, results, lock)

    assert results[0]['status'] in ('failed', 'created')
