from datetime import datetime
from flask import Flask, request, jsonify, make_response

from os import environ
from models import db, PurchaseAgreement, Vendor, PlantType, PurchaseOrder, Plant

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("DB_URL")
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/", methods=["GET"])
def hello_world():
    return make_response(jsonify({"message": "hello world"}), 200)


# create vendor
@app.route("/vendor", methods=["POST"])
def create_vendor():
    try:
        data = request.get_json()
        new_v = Vendor(name=data["name"])
        db.session.add(new_v)
        db.session.commit()
        return make_response(jsonify({"message": "vendor created"}), 201)
    except Exception as err:
        return make_response(jsonify({"message": f"error creating vendor: {err}"}), 500)


# create plant_type
@app.route("/plant_type", methods=["POST"])
def create_plant_type():
    try:
        data = request.get_json()
        new_pt = PlantType(name=data["name"])
        db.session.add(new_pt)
        db.session.commit()
        return make_response(jsonify({"message": "plant_type created"}), 201)
    except Exception as err:
        return make_response(
            jsonify({"message": f"error creating plant_type: {err}"}), 500
        )


# create a purchase_agreement
@app.route("/purchase_agreement", methods=["POST"])
def create_purchase_agreement():
    try:
        data = request.get_json()
        pt = db.session.query(PlantType).get(data["plant_type_id"])
        v = db.session.query(Vendor).get(data["vendor_id"])
        new_pa = PurchaseAgreement(
            total_quantity=data["total_quantity"],
            end_date=data["end_date"],
            vendor=v,
            plant_type=pt,
        )
        db.session.add(new_pa)
        db.session.commit()
        return make_response(jsonify({"message": "purchase_agreement created"}), 201)
    except Exception as err:
        return make_response(
            jsonify({"message": f"error creating purchase_agreement: {err}"}), 500
        )


@app.route("/purchase_order/agreement/<int:id>", methods=["POST"])
def create_purchase_order_with_agreement(id):
    try:
        pa = PurchaseAgreement.query.filter_by(id=id).first()
        if pa:
            data = request.get_json()
            new_quantity = data["quantity"]
            pos_quantity_total = sum(po.quantity for po in pa.purchase_orders)

            max_allowed_quantity = pa.total_quantity - pos_quantity_total

            if datetime.now() > pa.end_date:
                return make_response(
                    jsonify({"message": "purchase_agreement past end_date"}), 400
                )

            if new_quantity > max_allowed_quantity:
                message = f"purchase_order quantity is too large. Max allowed is {max_allowed_quantity}"

                if max_allowed_quantity == 0:
                    message = "purchase_agreement filled."

                return make_response(jsonify({"message": message}), 400)

            new_po = PurchaseOrder(
                quantity=data["quantity"],
                vendor=pa.vendor,
                plant_type=pa.plant_type,
                purchase_agreement=pa,
            )
            db.session.add(new_po)
            db.session.commit()
            return make_response(jsonify({"message": "purchase_order created"}), 201)

        return make_response(jsonify({"message": "purchase_agreement not found"}), 404)
    except Exception as err:
        return make_response(
            jsonify({"message": f"error creating purchase_order: {err}"}), 500
        )


@app.route("/purchase_order", methods=["POST"])
def create_purchase_order():
    try:
        data = request.get_json()
        pt = db.session.query(PlantType).get(data["plant_type_id"])
        v = db.session.query(Vendor).get(data["vendor_id"])
        new_po = PurchaseOrder(quantity=data["quantity"], vendor=v, plant_type=pt)
        db.session.add(new_po)
        db.session.commit()
        return make_response(jsonify({"message": "purchase_order created"}), 201)
    except Exception as err:
        return make_response(
            jsonify({"message": f"error creating purchase_order: {err}"}), 500
        )


# update a purchase_order
@app.route("/purchase_order/<int:id>", methods=["PUT"])
def update_purchase_order(id):
    try:
        purchase_order = PurchaseOrder.query.filter_by(id=id).first()
        if purchase_order:
            if not purchase_order.is_received:
                data = request.get_json()
                purchase_order.is_received = data["received"]

                new_plant = Plant(plant_type=purchase_order.plant_type)
                db.session.add(new_plant)
                db.session.commit()
                return make_response(
                    jsonify({"message": "purchase_order updated"}), 200
                )
            return make_response(
                jsonify({"message": "purchase_order already received"}), 400
            )
        return make_response(jsonify({"message": "purchase_order not found"}), 404)
    except Exception as err:
        return make_response(
            jsonify({"message": f"error updating purchase_order: {err}"}), 500
        )
