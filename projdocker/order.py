from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from invokes import invoke_http
from os import environ
import sqlalchemy

app = Flask(__name__)
CORS(app)

engine = sqlalchemy.create_engine(environ.get('dbURL'), echo=True)
orders_table = sqlalchemy.Table(
    "orders",
    sqlalchemy.MetaData(),
    sqlalchemy.Column("order_id", sqlalchemy.Integer),
    sqlalchemy.Column("listing_id", sqlalchemy.Integer),
    sqlalchemy.Column("buyqty", sqlalchemy.Float(precision=2)),
    sqlalchemy.Column("buyerphone", sqlalchemy.Integer),
    sqlalchemy.Column("price", sqlalchemy.Float(precision=2)),
    sqlalchemy.Column("buyeremail", sqlalchemy.String(64)),
    sqlalchemy.Column("selleremail", sqlalchemy.String(64)),
    sqlalchemy.Column("paymenttoken", sqlalchemy.String(182)),
    sqlalchemy.Column("googlepay", sqlalchemy.Boolean)
)

@app.route("/order", methods=['POST'])
def order():
    data = request.get_json();
    print(data)
    stmt = sqlalchemy.insert(orders_table).values(order_id="", listing_id=data['listing_id'], buyqty=data['buyqty'], buyerphone=data['buyerphone'], price=data['price'], buyeremail=data['buyeremail'], selleremail=data['selleremail'], paymenttoken=data['paymentToken'], googlepay=data['googlepay'])
    compiled = stmt.compile()
    with engine.connect() as conn:
        result = conn.execute(stmt)
    print(result)
    if result:
        return jsonify({'code': 200, 'data':True}, 200)
    else:
        return jsonify({'code': 500, 'message':"Internal Server error"}, 500)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)
