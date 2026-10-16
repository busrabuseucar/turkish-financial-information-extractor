import json
import subprocess
import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from app.api import app
from scripts.evaluate import evaluate

client = TestClient(app)
ROOT = Path(__file__).resolve().parents[1]


def test_api_and_cli_agree():
    text = '120 ay vadeli ve %3,19 kâr payı'
    response = client.post('/extract', json={'text': text})
    assert response.status_code == 200
    p = subprocess.run([sys.executable, '-m', 'turfinextract.cli', text], capture_output=True, text=True, check=True, cwd='/tmp')
    assert json.loads(p.stdout) == response.json()
    assert client.get('/health').json() == {'status': 'ok'}


@pytest.mark.parametrize('payload,status', [({}, 422), ({'text': ''}, 422), ({'text': ' '}, 400), ({'text': 'a' * 20001}, 422), ({'text': 123}, 422)])
def test_bad_api_requests(payload, status):
    assert client.post('/extract', json=payload).status_code == status


def test_cli_invalid_input():
    p = subprocess.run([sys.executable, '-m', 'turfinextract.cli', ' '], capture_output=True, text=True)
    assert p.returncode == 2
    assert p.stdout == ''
    assert 'Traceback' not in p.stderr


def test_empty_evaluation_rejected(tmp_path):
    path = tmp_path / 'empty.jsonl'
    path.write_text('')
    with pytest.raises(ValueError, match='empty'):
        evaluate(path)


def test_fixture_report_is_reproducible():
    a = evaluate(ROOT / 'data/benchmark.jsonl')
    b = evaluate(ROOT / 'data/benchmark.jsonl')
    assert a == b
    assert a['examples'] == 30
    assert a['micro']['tp'] > 0
    assert len(a['dataset_sha256']) == 64


def test_streamlit_extract_flow():
    from streamlit.testing.v1 import AppTest
    app = AppTest.from_file(str(ROOT / 'app/streamlit_app.py')).run(timeout=30)
    assert not app.exception
    app.button[0].click().run(timeout=30)
    assert not app.exception
    assert len(app.json) == 1
    assert '2500000' in app.json[0].value
