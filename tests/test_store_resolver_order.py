from pathlib import Path

def test_get_store_signature_order():
    text = Path('src/fabricops_kit/config.py').read_text(encoding='utf-8')
    assert 'def _get_store(config: FrameworkConfig | PathConfig | None, env: str, target: str)' in text

def test_io_helpers_call_get_store_in_config_env_target_order():
    text = Path('src/fabricops_kit/fabric_input_output.py').read_text(encoding='utf-8')
    assert '_get_store(config, env, target)' in text
    assert '_get_store(env, target, config)' not in text

