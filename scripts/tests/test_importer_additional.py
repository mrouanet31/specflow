import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytest

from scripts.github_issue_importer import issue_exists, ensure_label, ensure_milestone, create_issue


class R:
    def __init__(self, status_code=200, json_data=None, text=''):
        self.status_code = status_code
        self._json = json_data or {}
        self.text = text

    def json(self):
        return self._json


class SessionMock:
    def __init__(self):
        self.posts = []
        self.gets = []

    def get(self, url, params=None):
        self.gets.append((url, params))
        # simulate search failure
        if url.endswith('/search/issues'):
            return R(status_code=500, text='err')
        # simulate existing label
        if '/labels/' in url:
            return R(status_code=200, json_data={'name': url.split('/')[-1]})
        # milestones list
        if url.endswith('/milestones'):
            return R(status_code=200, json_data=[{'title': 'S1', 'number': 7}])
        return R(status_code=404)

    def post(self, url, json=None):
        self.posts.append((url, json))
        # default create issue success
        if url.endswith('/issues'):
            return R(status_code=201, json_data={'html_url': 'https://github.com/fake/1'})
        return R(status_code=201, json_data={})


def test_issue_exists_raises_on_search_error():
    s = SessionMock()
    with pytest.raises(RuntimeError):
        issue_exists(s, 'owner/repo', 'title')


def test_ensure_label_returns_true_when_existing():
    s = SessionMock()
    res = ensure_label(s, 'owner/repo', 'bug')
    assert res is True


def test_ensure_milestone_finds_existing_and_returns_number():
    s = SessionMock()
    num = ensure_milestone(s, 'owner/repo', 'S1')
    assert num == 7


def test_create_issue_parses_labels_and_assignees_and_milestone():
    s = SessionMock()
    r = create_issue(s, 'owner/repo', 'T', 'B', labels='a; b', assignee='alice', milestone=3, verbose=True)
    assert r.status_code == 201
    # check that the POST payload for issues was captured and has expected structure
    found = False
    for url, payload in s.posts:
        if url.endswith('/issues'):
            assert payload['title'] == 'T'
            assert 'labels' in payload and payload['labels'] == ['a', 'b']
            assert payload['assignees'] == ['alice']
            assert payload['milestone'] == 3
            found = True
    assert found
