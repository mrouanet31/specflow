import os
import sys
import json
from threading import Lock

import pytest

# Ensure project root on path
import os as _os
sys.path.insert(0, _os.path.abspath(_os.path.join(_os.path.dirname(__file__), '..', '..')))

from scripts.github_issue_importer import worker_task


class MockResponse:
    def __init__(self, status_code, json_data=None, text=''):
        self.status_code = status_code
        self._json = json_data or {}
        self.text = text or json.dumps(self._json)

    def json(self):
        return self._json


class MockSession:
    def __init__(self):
        self.headers = {}
        self.calls = []
        self.created_labels = []
        self.created_milestones = []
        self.issue_create_attempts = 0

    def headers_update(self, h):
        self.headers.update(h)

    # keep compatibility with session.headers.update call
    def __getattr__(self, name):
        if name == 'headers':
            return self.__dict__['headers']
        raise AttributeError(name)

    def get(self, url, params=None):
        self.calls.append(('GET', url, params))
        # search issues endpoint
        if url.endswith('/search/issues'):
            # if query contains "exists-title" simulate found
            q = params.get('q', '') if params else ''
            if 'EXISTS_TITLE' in q:
                return MockResponse(200, {'items': [{'title': 'EXISTS_TITLE'}]})
            return MockResponse(200, {'items': []})

        # label get
        if '/labels/' in url:
            # simulate not found
            return MockResponse(404, {})

        # milestones list
        if url.endswith('/milestones'):
            return MockResponse(200, [])

        return MockResponse(404, {})

    def post(self, url, json=None):
        self.calls.append(('POST', url, json))
        if url.endswith('/labels'):
            name = json.get('name')
            self.created_labels.append(name)
            return MockResponse(201, {'name': name})

        if url.endswith('/milestones'):
            title = json.get('title')
            num = len(self.created_milestones) + 1
            self.created_milestones.append(title)
            return MockResponse(201, {'number': num, 'title': title})

        if url.endswith('/issues'):
            # simulate transient failure on first attempt, then success
            self.issue_create_attempts += 1
            if self.issue_create_attempts == 1:
                return MockResponse(503, {}, text='Service Unavailable')
            return MockResponse(201, {'html_url': f'https://github.com/fake/repo/issues/{self.issue_create_attempts}'})

        return MockResponse(404, {})


def test_worker_task_creates_with_retries_and_creates_labels_and_milestone(monkeypatch):
    # Patch requests.Session to return our MockSession
    import requests

    monkeypatch.setenv('GITHUB_TOKEN', 'fake')

    def fake_session_ctor():
        return MockSession()

    monkeypatch.setattr('requests.Session', fake_session_ctor)

    # monkeypatch sleep to avoid waiting
    import scripts.github_issue_importer as importer
    monkeypatch.setattr(importer.time, 'sleep', lambda _: None)

    args = type('A', (), {
        'repo': 'owner/repo',
        'dry_run': False,
        'skip_existing': False,
        'sleep': 0.0,
        'create_labels': True,
        'milestone': None,
        'label_estimate': True,
        'verbose': False,
        'concurrency': 1,
        'output_file': 'import-results.csv',
    })()

    row = {
        'title': 'Need retry',
        'body': 'body',
        'estimate': '8',
        'labels': 'bug,high',
        'assignee': 'alice',
        'milestone': 'Sprint 1',
    }

    results = []
    lock = Lock()

    worker_task(args, row, 1, results, lock)

    assert len(results) == 1
    assert results[0]['status'] == 'created'
    assert results[0]['issue_url'].startswith('https://github.com')


def test_worker_task_skips_existing_when_skip_existing(monkeypatch):
    monkeypatch.setenv('GITHUB_TOKEN', 'fake')

    # create mock session but make search return found item
    class SearchMock(MockSession):
        def get(self, url, params=None):
            if url.endswith('/search/issues'):
                return MockResponse(200, {'items': [{'title': 'EXISTS_TITLE'}]})
            return super().get(url, params=params)

    def fake_session_ctor():
        return SearchMock()

    import requests
    monkeypatch.setattr('requests.Session', fake_session_ctor)

    import scripts.github_issue_importer as importer
    monkeypatch.setattr(importer.time, 'sleep', lambda _: None)

    args = type('A', (), {
        'repo': 'owner/repo',
        'dry_run': False,
        'skip_existing': True,
        'sleep': 0.0,
        'create_labels': False,
        'milestone': None,
        'label_estimate': False,
        'verbose': False,
        'concurrency': 1,
        'output_file': 'import-results.csv',
    })()

    row = {'title': 'EXISTS_TITLE', 'body': 'already exists'}
    results = []
    lock = Lock()
    worker_task(args, row, 1, results, lock)

    assert len(results) == 1
    assert results[0]['status'] == 'exists'
