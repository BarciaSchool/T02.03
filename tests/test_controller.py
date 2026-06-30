def test_get_vacio(client):
    r = client.get("/api/v1/categorias")
    assert r.status_code == 200
    assert r.json() == {"data": [], "errors": []}


def test_post_crea(client):
    r = client.post("/api/v1/categorias", json={"nombre": "Tecnología", "descripcion": "x"})
    assert r.status_code == 201
    assert r.json()["data"][0]["nombre"] == "Tecnología"


def test_get_por_id(client):
    client.post("/api/v1/categorias", json={"nombre": "A", "descripcion": "a"})
    r = client.get("/api/v1/categorias/1")
    assert r.status_code == 200


def test_get_por_id_404(client):
    r = client.get("/api/v1/categorias/999")
    assert r.status_code == 404
    assert r.json()["errors"][0]["codigo"] == 404


def test_put_actualiza(client):
    client.post("/api/v1/categorias", json={"nombre": "A", "descripcion": "a"})
    r = client.put("/api/v1/categorias/1", json={"nombre": "B", "descripcion": "b"})
    assert r.status_code == 200
    assert r.json()["data"][0]["nombre"] == "B"


def test_put_404(client):
    r = client.put("/api/v1/categorias/999", json={"nombre": "B", "descripcion": "b"})
    assert r.status_code == 404


def test_delete(client):
    client.post("/api/v1/categorias", json={"nombre": "A", "descripcion": "a"})
    r = client.delete("/api/v1/categorias/1")
    assert r.status_code == 200


def test_delete_404(client):
    r = client.delete("/api/v1/categorias/999")
    assert r.status_code == 404


def test_validacion_422(client):
    r = client.post("/api/v1/categorias", json={"descripcion": "sin nombre"})
    assert r.status_code == 422


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}
