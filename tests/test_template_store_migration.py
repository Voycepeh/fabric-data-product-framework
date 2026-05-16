from pathlib import Path
import json

NB_DIR = Path('templates/notebooks')

def _all_source_text():
    out=[]
    for p in NB_DIR.glob('*.ipynb'):
        d=json.loads(p.read_text(encoding='utf-8'))
        for c in d.get('cells',[]):
            out.append(''.join(c.get('source',[])))
    return '\n'.join(out)

def test_templates_do_not_contain_legacy_tokens():
    text=_all_source_text()
    assert 'Housepath' not in text
    assert 'get_path(' not in text
    assert 'AI_ENABLED' not in text
    assert '_get_store(' not in text

def test_00_env_config_has_fabricstore_keywords():
    d=json.loads(Path('templates/notebooks/00_env_config.ipynb').read_text(encoding='utf-8'))
    t='\n'.join(''.join(c.get('source',[])) for c in d['cells'])
    assert 'FabricStore(env="dev"' in t
    assert 'kind="lakehouse"' in t
    assert 'kind="warehouse"' in t

def test_notebook_code_cells_compile():
    for p in NB_DIR.glob('*.ipynb'):
        d=json.loads(p.read_text(encoding='utf-8'))
        for c in d.get('cells',[]):
            if c.get('cell_type')!='code':
                continue
            src=''.join(c.get('source',[]))
            if src.strip():
                compile(src, f'{p.name}', 'exec')
