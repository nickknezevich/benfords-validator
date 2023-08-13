import json
import pytest
from ..models import User

#test failing, probably because of the different instance.
def test_hc(test_app):
    client = test_app.test_client()
    res = client.get('/api/hc')
    assert res.status_code == 200
    expected = {'status': 'ok'}
    assert expected == json.loads(res.get_data(as_text=True))