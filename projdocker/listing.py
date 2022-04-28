from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS
import json


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)

class Listing(db.Model):
    __tablename__ = 'listing'

    listing_id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Float(precision=2))
    currqty = db.Column(db.Float(precision=2))
    postTime = db.Column(db.DateTime, nullable=False)
    startTime = db.Column(db.DateTime, nullable=False)
    endTime = db.Column(db.DateTime, nullable=False)
    productName = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(256), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    category = db.Column(db.String(64), nullable=False)
    availability = db.Column(db.Boolean, nullable=False)
    location = db.Column(db.String(64), nullable=False)
    unit = db.Column(db.String(16), nullable=False)
    phoneNumber = db.Column(db.String(8), nullable=False)
    sellername = db.Column(db.String(64))
    selleremail = db.Column(db.String(64))
    image = db.Column(db.String(256))

    def __init__(self, listing_id, quantity, currqty, postTime, startTime , endTime, productName, description, price, category, availability, location, unit, phoneNumber, sellername, selleremail, image):
        self.listing_id = listing_id
        self.quantity = quantity
        self.currqty = currqty
        self.postTime = postTime
        self.startTime = startTime
        self.endTime = endTime
        self.productName = productName
        self.description = description
        self.price = price
        self.category = category
        self.availability = availability
        self.location = location
        self.unit = unit
        self.phoneNumber = phoneNumber
        self.sellername = sellername
        self.selleremail = selleremail
        self.image = image

    def json(self):
        return {"listing_id": self.listing_id, "quantity": self.quantity, "currqty": self.currqty, "postTime": self.postTime , "startTime": self.startTime, "endTime": self.endTime, "productName" : self.productName, "description": self.description, "price": self.price, "category":self.category,"availability":self.availability,"location":self.location, "unit":self.unit, "phoneNumber": self.phoneNumber, "sellername": self.sellername, "selleremail": self.selleremail, "image": self.image}

@app.route("/listing")
def get_all_listings():
    listinglist = Listing.query.all()
    if len(listinglist):
        return jsonify(
            {
                "code": 200,
                "data": [list.json() for list in listinglist]
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no listings."
        }
    ), 404

@app.route("/listing/<string:lid>")
def find_by_id(lid):
    products = Listing.query.filter(Listing.listing_id.like(lid)).all()
    if products == []:
        return jsonify(
            {
                "code": 404,
                "message": "Product not found."
            }
        ), 404
    else:
        return jsonify(
            {
                "code": 200,
                "data": products[0].json()
            }
        )

@app.route("/listing/productname/<string:productName>")
def find_by_productName(productName):
    products = Listing.query.filter(Listing.productName.like("%"+productName+"%")).all()
    if products == []:
        return jsonify(
            {
                "code": 404,
                "message": "Product not found."
            }
        ), 404
    else:
        return jsonify(
            {
                "code": 200,
                "data": [p.json() for p in products]
            }
        )

@app.route("/listing/findbyname/<string:name>")
def find_by_seller(name):
    products = Listing.query.filter(Listing.sellername.like(name)).all()
    if products == []:
        return jsonify(
            {
                "code": 404,
                "message": "Product(s) not found."
            }
        ), 404
    else:
        return jsonify(
            {
                "code": 200,
                "data": [p.json() for p in products]
            }
        )

#When adding, generate pk
@app.route("/listing", methods=['POST'])
def create_listing():
    data = request.get_json()
    listing = Listing("", **data) #any data that is being sent
    try:
        db.session.add(listing)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "listing_id": listing_id
                },
                "message": "An error occurred creating the listing."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": True
        }
    ), 201

# update by ID (is ok cause will be listed on user's profile page they can just link to id and click all)
@app.route("/listing/<string:listing_id>", methods=['POST'])
def update_listing(listing_id):
    listing = Listing.query.filter_by(listing_id = listing_id).first()
    if listing:
        data = request.get_json()
        if data['startTime']:
            listing.startTime = data['startTime']
        if data['endTime']:
            listing.endTime = data['endTime']
        if data['productName']:
            listing.productName = data['productName']
        if data['description']:
            listing.description = data['description']
        if data['price']:
            listing.price = data['price']
        if data['category']:
            listing.category = data['category']
        if data['availability']:
            listing.availability = data['availability']
        if data['location']:
            listing.location = data['location']
        if data['unit']:
            listing.unit = data['unit']
        if data['phoneNumber']:
            listing.phoneNumber = data['phoneNumber']
        if data['quantity']:
            listing.quantity = data['quantity']
        if data['currqty']:
            listing.currqty = data['currqty']

        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": listing.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "listing_id": listing_id
            },
            "message": "Product not found."
        }
    ), 404


# Done
@app.route("/listing/<string:listing_id>", methods=['DELETE'])
def delete_listing(listing_id):
    listing = Listing.query.filter_by(listing_id=listing_id).first()
    if listing:
        db.session.delete(listing)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": {
                    "listing_id": listing_id
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "listing_id": listing_id
            },
            "message": "Product not found."
        }
    ), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
