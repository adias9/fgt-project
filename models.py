from app import db


class Vendor(db.Model):
    __tablename__ = 'vendor'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    purchase_agreements = db.relationship(
        'PurchaseAgreement',
        backref=db.backref('vendor', lazy='joined'),
        lazy=True
    )
    purchase_orders = db.relationship(
        'PurchaseOrder',
        backref=db.backref('vendor', lazy='joined'),
        lazy=True
    )


class PurchaseAgreement(db.Model):
    __tablename__ = 'purchase_agreement'

    id = db.Column(db.Integer, primary_key=True)
    total_quantity = db.Column(db.Integer, default=0)
    end_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, 
        server_default=db.func.now(),
        server_onupdate=db.func.now()
    )
    vendor_id = db.Column(
        db.Integer,
        db.ForeignKey('vendor.id'),
        nullable=False
    )
    purchase_orders = db.relationship(
        'PurchaseOrder',
        backref=db.backref('vendor', lazy='joined'),
        lazy=True
    )


class PurchaseOrder(db.Model):
    __tablename__ = 'purchase_order'

    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, default=0)
    is_received = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, 
        server_default=db.func.now(),
        server_onupdate=db.func.now()
    )
    plant_type_id = db.Column(
        db.Integer,
        db.ForeignKey('plant_type.id'),
        nullable=False
    )
    vendor_id = db.Column(
        db.Integer,
        db.ForeignKey('vendor.id'),
        nullable=False
    )
    purchase_agreement_id = db.Column(
        db.Integer,
        db.ForeignKey('purchase_agreement.id'),
        nullable=True
    )


class PlantType(db.Model):
    __tablename__ = 'plant_type'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    purchase_orders = db.relationship(
        PurchaseOrder,
        backref=db.backref('plant_type', lazy='joined'),
        lazy=True
    )
    plants = db.relationship(
        'Plant',
        backref=db.backref('plant_type', lazy='joined'),
        lazy=True
    )


class Plant(db.Model):
    __tablename__ = 'plant'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    plant_type_id = db.Column(
        db.Integer,
        db.ForeignKey('plant_type.id'),
        nullable=False
    )
