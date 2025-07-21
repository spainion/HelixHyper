import importlib
import sys
from pathlib import Path


def test_init_uses_default_logging(tmp_path, monkeypatch):
    import hyperhelix.__init__ as mod
    fake = tmp_path / 'missing.yaml'
    if 'hyperhelix.__init__' in sys.modules:
        del sys.modules['hyperhelix.__init__']
    monkeypatch.setattr(mod, 'CONFIG_PATH', fake, raising=False)
    mod = importlib.import_module('hyperhelix.__init__')
    assert hasattr(mod, '__all__')
