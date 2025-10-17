import os
import sys
from threading import Lock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from scripts.github_issue_importer import worker_task


def test_worker_task_with_requests_mock(requests_mocker, monkeypatch):
    monkeypatch.setenv('GITHUB_TOKEN', 'fake')

    # Mock label GET to return 404 -> force creation
    requests_mocker.get('https://api.github.com/repos/owner/repo/labels/bug', status_code=404, json={})
    requests_mocker.post('https://api.github.com/repos/owner/repo/labels', status_code=201, json={'name': 'bug'})

    # Mock milestones list and creation
    requests_mocker.get('https://api.github.com/repos/owner/repo/milestones', status_code=200, json=[])
    requests_mocker.post('https://api.github.com/repos/owner/repo/milestones', status_code=201, json={'number': 1})

    # Mock issue creation: first returns 503, then 201
    # We use a simple counter in the callback
    call_state = {'count': 0}

    def issue_callback(request, context):
        call_state['count'] += 1
        if call_state['count'] == 1:
            context.status_code = 503
            return {}
        context.status_code = 201
        return {'html_url': 'https://github.com/owner/repo/issues/1'}

    requests_mocker.post('https://api.github.com/repos/owner/repo/issues', json=issue_callback)

    args = type('A', (), {
        'repo': 'owner/repo', 'dry_run': False, 'skip_existing': False, 'sleep': 0.0,
        'create_labels': True, 'milestone': None, 'label_estimate': True, 'verbose': False,
        'concurrency': 1, 'output_file': 'import-results.csv'
    })()

    row = {'title': 'Mocked', 'body': 'body', 'estimate': '2', 'labels': 'bug', 'assignee': 'alice', 'milestone': 'S1'}
    results = []
    lock = Lock()
    worker_task(args, row, 1, results, lock)

    assert len(results) == 1
    assert results[0]['status'] == 'created'
    assert 'github.com' in results[0]['issue_url']
