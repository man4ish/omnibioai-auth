def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_metrics(client):
    resp = client.get("/metrics")
    assert resp.status_code == 200
    assert b"jwt_auth_total" in resp.content
