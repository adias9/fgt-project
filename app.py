from flask import Flask, request, jsonify, make_response

from os import environ
from models import db, PurchaseAgreement, Vendor, PlantType

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/', methods=['GET'])
def hello_world():
    return make_response(jsonify({'message': 'hello world'}), 200)


# create vendor
@app.route('/vendor', methods=['POST'])
def create_vendor():
    try:
        data = request.get_json()
        new_v = Vendor(name=data['name'])
        db.session.add(new_v)
        db.session.commit()
        return make_response(
            jsonify({'message': 'vendor created'}),
            201
        )
    except Exception as err:
        return make_response(
            jsonify({'message': f'error creating vendor: {err}'}), 
            500
        )


# create plant_type
@app.route('/plant_type', methods=['POST'])
def create_plant_type():
    try:
        data = request.get_json()
        new_pt = PlantType(name=data['name'])
        db.session.add(new_pt)
        db.session.commit()
        return make_response(
            jsonify({'message': 'plant_type created'}),
            201
        )
    except Exception as err:
        return make_response(
            jsonify({'message': f'error creating plant_type: {err}'}), 
            500
        )


# create a purchase_agreement
@app.route('/purchase_agreement', methods=['POST'])
def create_purchase_agreement():
    try:
        data = request.get_json()
        v = db.session.query(Vendor).get(data['vendor_id'])
        new_pa = PurchaseAgreement(
            total_quantity=data['total_quantity'],
            end_date=data['end_date'],
            vendor=v
        )
        db.session.add(new_pa)
        db.session.commit()
        return make_response(
            jsonify({'message': 'purchase_agreement created'}),
            201
        )
    except Exception:
        return make_response(
            jsonify({'message': 'error creating purchase_agreement'}), 
            500
        )


# update a user
# @app.route('/users/<int:id>', methods=['PUT'])
# def update_user(id):
#     try:
#         user = User.query.filter_by(id=id).first()
#         if user:
#             data = request.get_json()
#             user.username = data['username']
#             user.email = data['email']
#             db.session.commit()
#             return make_response(jsonify({'message': 'user updated'}), 200)
#         return make_response(jsonify({'message': 'user not found'}), 404)
#     except Exception:
#         return make_response(jsonify({'message': 'error updating user'}), 500)

