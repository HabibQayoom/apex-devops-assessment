from app import db


def test_health_is_ok(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_ready_when_database_is_up(client):
    r = client.get("/ready")
    assert r.status_code == 200
    assert r.json()["status"] == "ready"


def test_create_and_list_operations(client):
    created = client.post("/operations", json={"title": "Rotate logs"})
    assert created.status_code == 201
    assert created.json()["status"] == "open"
    listed = client.get("/operations").json()
    assert [o["title"] for o in listed] == ["Rotate logs"]


def test_get_missing_operation_returns_404(client):
    assert client.get("/operations/999").status_code == 404


def test_empty_title_is_rejected(client):
    assert client.post("/operations", json={"title": ""}).status_code == 422


def test_update_status(client):
    op = client.post("/operations", json={"title": "Patch node"}).json()
    r = client.patch(f"/operations/{op['id']}/status", json={"status": "done"})
    assert r.status_code == 200
    assert r.json()["status"] == "done"


def test_invalid_status_is_rejected(client):
    op = client.post("/operations", json={"title": "x"}).json()
    r = client.patch(f"/operations/{op['id']}/status", json={"status": "bogus"})
    assert r.status_code == 422


def test_metrics_endpoint_exposes_request_counter(client):
    client.get("/health")
    body = client.get("/metrics").text
    assert "http_requests_total" in body
    assert "app_db_up" in body


def test_ready_returns_503_when_database_is_down(client, monkeypatch):
    monkeypatch.setattr(db, "check_db", lambda engine: False)
    r = client.get("/ready")
    assert r.status_code == 503
    assert r.json()["reason"] == "database unavailable"


def test_simulated_bad_release_fails_readiness(client, monkeypatch):
    monkeypatch.setenv("SIMULATE_BAD_RELEASE", "true")
    assert client.get("/ready").status_code == 503


def test_version_endpoint(client, monkeypatch):
    assert "version" in client.get("/version").json()
