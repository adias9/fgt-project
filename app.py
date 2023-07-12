from flask import Flask, request, jsonify, make_response

from os import environ
from models import db, PurchaseAgreement, Vendor

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/', methods=['GET'])
def hello_world():
    return make_response(jsonify({'message': 'hello world'}), 200)


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

