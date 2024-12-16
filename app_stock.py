
# Structure de base fournie :
from dataclasses import dataclass
from typing import List

from plotly.data import stocks


@dataclass
class OrderItem:
    product_id: str
    quantity: int


@dataclass
class Order:
    order_id: str
    customer_id: str
    items: List[OrderItem]
    status: str


# À vous de compléter :
from flask import Flask, jsonify, request

app = Flask(__name__)

orders = {}
Products = {
    "PROD001": {"name": "oridnateur", "stock": 5},
    "PROD002": {"name": "imprimante", "stock": 4},
    "PROD003": {"name": "clavier", "stock": 10},
}


@app.route("/api/orders", methods=["POST"])
def create_order():
    # TODO: Implémenter la création de commande
    data = request.json
    if "order_id" not in data or "customer_id" not in data or "items" not in data:
        return (
            jsonify(
                {
                    "error": "l'order de la commande ou l'id du client ou les produits ne sont pas saisis"
                }
            ),
            400,
        )

    order_id = data.get("order_id")
    customer_id = data["customer_id"]
    items = data.get("items")
    # verifier que les produits existent dans le stock avec une quantite suffisante

    for item in items:
        if "quantity" not in item:
            return jsonify({f"error": "la quantite du produit n'est pas saisie"}), 400
        if "product_id" not in item:
            return jsonify({f"error": "l'id du produit n'est pas saisi"}), 400
        if type(item["quantity"]) != int or item["quantity"] < 0:
            return (
                jsonify(
                    {
                        "error": "la quantité d'un produit est un entier positif",
                        "status": "echec",
                    }
                ),
                400,
            )
        if item["product_id"] not in Products:
            return (
                jsonify(
                    {
                        "error": f"l'item {item['product_id']} est introuvable",
                        "status": "echec",
                    }
                ),
                404,
            )
        elif item["quantity"] > Products[item["product_id"]]["stock"]:
            return jsonify({"error": "Stock insufisant", "status": "echec"}), 400

    # apres s'assurer que les produits existent en quantite suffisante on crée la commande
    status = "Valide"
    order = Order(order_id, customer_id, items, status)
    orders[order.order_id] = order

    # mise a jour du stock
    for item in items:
        Products[item["product_id"]]["stock"] -= item["quantity"]

    return (
        jsonify(
            {
                "message": f"hello! votre commande d'id {order_id} est envoyée",
                "status": status,
            }
        ),
        201,
    )


@app.route("/api/<reference>/<quantite>", methods=["GET"])
def update_stock(reference, quantite):
    try:
        if reference in Products:
            Products[reference]["stock"] += int(quantite)
        else:
            Products[reference]["stock"] = int(quantite)
            Products[reference]["name"] = "unkown"
        return jsonify({reference: Products[reference]["stock"]}), 200
    except ValueError:
        return jsonify({"error": "la quantite du produit doit etre un entier !"}), 400


@app.route("/api/<reference>", methods=["PUT"])
def update_qstock(reference):
    if reference not in Products:
        return jsonify({"Error": "le produit est introuvable"}), 400
    else:
        if "quantite" not in request.json:
            return jsonify({"error": "quantite n'est pas saisie"}), 400
        else:
            quantite = request.json["quantite"]
            if not isinstance(quantite, int):
                return (
                    jsonify({"error": "la quantite d'un produit doit etre un entier"}),
                    400,
                )
            if quantite < 0:
                return (
                    jsonify(
                        {"error": "la quantite d'un produit ne peut pas etre négative"}
                    ),
                    400,
                )
            else:
                Products[reference]["stock"] = quantite
                return jsonify({"message": "Produit mis a jour avec succès"}), 200


@app.route("/api/orders/<order_id>", methods=["GET"])
def get_order(order_id):
    # TODO: Implémenter la récupération de commande
    try:
        order = orders[order_id]
        customer_id = order.customer_id
        items = order.items
        status = order.status
        return (
            jsonify(
                {
                    "order_id": order_id,
                    "customer_id": customer_id,
                    "items": [
                        {"product_id": item["product_id"], "quantity": item["quantity"]}
                        for item in items
                    ],
                    "status": status,
                }
            ),
            200,
        )
    except KeyError as e:
        return jsonify({"error": f"la commande {e} n'existe pas"})


@app.route("/api/stock/<reference>", methods=["GET"])
def get_stock(reference):
    if reference not in Products:
        return jsonify({"error": "Le produit est introuvable"}), 400
    name = Products[reference]["name"]
    stock = Products[reference]["stock"]
    return jsonify({"reference": reference, "name": name, "stock": stock}), 200


@app.route("/api/stock")
def liste_stock():
    return jsonify(
        [
            f"la liste des produits disponibles dans le  stock est {product['name']} avec une quantité égale à {product['stock']}"
            for product in Products.values()
        ]
    )


@app.route("/api/delete/<reference>", methods=["DELETE"])
def delete_prod(reference):
    try:
        del Products[reference]
        return jsonify({"message": f"le produit {reference} est supprimé"}), 200
    except KeyError:
        return jsonify({"error": "le produit n'existe pas pour le supprimer"}), 404


if __name__ == "__main__":
    app.run()


