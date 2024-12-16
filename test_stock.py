import pytest


from app_stock import app, Products


@pytest.fixture
def client():
    with app.test_client() as client:
        return client


# Tests
def test_create_order(client):
    # TODO: Implémenter les tests
    reponse = client.post(
        "/api/orders",
        json={
            "order_id": "ord1",
            "customer_id": "c1",
            "items": [{"product_id": "PROD001", "quantity": 2}],
        },
    )
    assert reponse.status_code == 201
    assert reponse.json["status"] == "Valide"
    reponse2 = client.post(
        "/api/orders",
        json={
            "order_id": "ord2",
            "customer_id": "c1",
            "items": [{"product_id": "PROD009", "quantity": 15}],
        },
    )
    assert reponse2.status_code == 400
    assert reponse2.json["error"] == f"l'item PROD009 est introuvable"
    reponse3 = client.post(
        "/api/orders",
        json={
            "order_id": "ord1",
            "customer_id": "c1",
            "items": [{"product_id": "PROD001", "quantity": -1}],
        },
    )
    assert reponse3.status_code == 400
    assert reponse3.json["status"] == "echec"
    assert reponse3.json["error"] == "la quantité d'un produit est un entier positif"


def test_get_orders(client):
    # TODO: Implémenter les tests
    reponse = client.get("/api/orders/ord1")
    assert reponse.status_code == 200
    reponse2 = client.get("/api/orders/ord3")
    assert reponse2.json["error"] == "la commande n'existe pas"


def test_update_stock(client):
    reponse = client.put("/api/PROD001", json={"quantite": 12})
    assert reponse.status_code == 200
    assert reponse.json["message"] == "Produit mis a jour avec succès"
    reponse2 = client.put("/api/PROD005", json={"quantite": 12})
    assert reponse2.json["Error"] == "le produit est introuvable"
    reponse3 = client.put("/api/PROD001", json={"quantite": "azrt"})
    assert reponse3.json["error"] == "la quantite d'un produit doit etre un entier"
    assert reponse3.status_code == 400
