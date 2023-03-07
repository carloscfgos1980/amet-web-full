from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, BOOLEAN
from flask_marshmallow import Marshmallow

app = Flask(__name__)
DB_NAME = "amet.db"
db = SQLAlchemy()
ma = Marshmallow(app)


app.config['SECRET_KEY'] = 'myKey'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
db.init_app(app)


class Painting(db.Model):
    __tablename__ = "paintings"

    paint_id = db.Column("paint_id", db.Integer, primary_key=True)
    title = db.Column("title", db.String(100))
    tech = db.Column("tech", db.String(100))
    size = db.Column("size", String(100))
    price = db.Column("price", db.Integer)
    img = db.Column("img", db.String)
    reserved = db.Column("reserved", db.BOOLEAN)
    sold = db.Column("sold", db.BOOLEAN)

    def __init__(self, paint_id, title, tech, size, price, img, reserved, sold):
        self.paint_id = paint_id
        self.title = title
        self.tech = tech
        self.size = size
        self.price = price
        self.img = img
        self.reserved = reserved
        self.sold = sold

    def __repr__(self):
        return f"({self.paint_id}) {self.title} {self.tech} {self.size} ({self.price}) {self.img} {self.reserved} {self.sold})"


class Customer(db.Model):
    __tablename__ = "customers"

    customer_id = db.Column("customer_id", db.Integer, primary_key=True)
    paint = db.Column(db.Integer, ForeignKey("paintings.paint_id"))
    name = db.Column("name", db.String(100))
    last_name = db.Column("last_name", db.String(100))
    country = db.Column("country", db.String(100))
    email = db.Column("email", db.String(100))
    comment = db.Column("comment", db.String(1000))

    def __init__(self, custumer_id, paint, name, last_name, country, email, comment):
        self.custumer_id = custumer_id
        self.paint = paint
        self.name = name
        self.last_name = last_name
        self.country = country
        self.email = email
        self.comment = comment

    def __repr__(self):
        return f"{self.customer_id} {self.paint} {self.name} {self.last_name} {self.country} {self.email} {self.comment}"


class Fan(db.Model):
    __tablename__ = "fans"

    customer_id = db.Column("customer_id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(100))
    last_name = db.Column("last_name", db.String(100))
    country = db.Column("country", db.String(100))
    email = db.Column("email", db.String(100))
    comment = db.Column("comment", db.String(1000))

    def __init__(self, custumer_id, name, last_name, country, email, comment):
        self.custumer_id = custumer_id
        self.name = name
        self.last_name = last_name
        self.country = country
        self.email = email
        self.comment = comment

    def __repr__(self):
        return f"{self.customer_id} {self.name} {self.last_name} {self.country} {self.email} {self.comment}"


class PaintingSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'tech', 'size',
                  'price', 'img', 'reserved', 'sold')


class CustomerSchema(ma.Schema):
    class Meta:
        fields = ('id', 'paint', 'name', 'last_name', 'country',
                  'email', 'comment')


class FanSchema(ma.Schema):
    class Meta:
        fields = ('customer_id', 'name', 'last_name', 'country',
                  'email', 'comment')


painting_schema = PaintingSchema()
paintings_schema = PaintingSchema(many=True)
customer_schema = CustomerSchema()
fan_schema = FanSchema()

with app.app_context():
    db.create_all()


@app.route('/painting', methods=['GET'])
def get_paintings():
    available_paintings = Painting.query.filter(Painting.sold == False)
    results = paintings_schema.dump(available_paintings)
    return jsonify(results)


@app.route('/painting/<id>', methods=['GET'])
def single_painting(id):
    painting = Painting.query.get(id)
    results = painting_schema.jsonify(painting)
    return results


@app.route('/customer', methods=['POST'])
def add_customer():
    paint = request.json['paint']
    name = request.json['name']
    last_name = request.json['last_name']
    country = request.json['country']
    email = request.json['email']
    comment = request.json['comment']

    customer = Customer(id, paint, name, last_name, country, email, comment)
    db.session.add(customer)
    db.session.commit()
    return customer_schema.jsonify(customer)


@app.route('/fan', methods=['POST'])
def add_fan():
    name = request.json['name']
    last_name = request.json['last_name']
    country = request.json['country']
    email = request.json['email']
    comment = request.json['comment']

    fan = Fan(id, name, last_name, country, email, comment)
    db.session.add(fan)
    db.session.commit()
    return fan_schema.jsonify(fan)


@app.route('/update/<id>', methods=['PATCH'])
def update_painting(id):
    painting = Painting.query.get(id)

    reserved = request.json['reserved']

    painting.reserved = reserved

    db.session.commit()
    results = painting_schema.jsonify(painting)
    return results


if __name__ == "__main__":
    app.run(debug=True)
