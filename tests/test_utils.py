from hyperhelix.utils import get_api_key


def test_get_api_key_env(monkeypatch):
    monkeypatch.setenv('MY_KEY', 'val')
    assert get_api_key('MY_KEY') == 'val'


def test_get_api_key_warning(monkeypatch, caplog):
    import logging

    logger = logging.getLogger('hyperhelix.utils')
    logger.propagate = True
    monkeypatch.delenv('MISSING_KEY', raising=False)
    assert get_api_key('MISSING_KEY') is None
    assert logger.isEnabledFor(logging.WARNING)
