from pathlib import Path

def test_env_example_has_placeholder():
    data = (Path(__file__).parents[1] / '.env.example').read_text()
    assert 'replace_with_your_new_api_key' in data
