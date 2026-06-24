def test_consultar_vacio(client):
    r = client.get("/api/v1/categorias")
    assert r.status_code == 200
    assert r.json() == {"data": [], "errors": []}


def test_crear_y_consultar(client):
    payload = {"nombre": "Tecnología", "descripcion": "Electrónicos"}
    r = client.post("/api/v1/categorias", json=payload)
    assert r.status_code == 201
    creada = r.json()["data"][0]
    assert creada["nombre"] == "Tecnología"
    assert creada["id"] == 1

    r2 = client.get("/api/v1/categorias")
    assert len(r2.json()["data"]) == 1


def test_buscar_por_id_no_existe(client):
    r = client.get("/api/v1/categorias/999")
    assert r.status_code == 404
    assert r.json()["errors"][0]["codigo"] == 404


def test_actualizar(client):
    client.post("/api/v1/categorias", json={"nombre": "A", "descripcion": "x"})
    r = client.put("/api/v1/categorias/1", json={"nombre": "B", "descripcion": "y"})
    assert r.status_code == 200
    assert r.json()["data"][0]["nombre"] == "B"


def test_eliminar(client):
    client.post("/api/v1/categorias", json={"nombre": "A", "descripcion": "x"})
    r = client.delete("/api/v1/categorias/1")
    assert r.status_code == 200
    r2 = client.get("/api/v1/categorias/1")
    assert r2.status_code == 404
