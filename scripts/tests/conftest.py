import pytest

try:
    import requests_mock as _requests_mock

    @pytest.fixture
    def requests_mocker():
        """Provide a requests-mock Mocker instance for tests.

        Uses the requests-mock library if installed.
        """
        with _requests_mock.Mocker() as m:
            yield m

except Exception:
    @pytest.fixture
    def requests_mocker():
        pytest.skip('requests-mock not installed; skipping requests-mock tests')
