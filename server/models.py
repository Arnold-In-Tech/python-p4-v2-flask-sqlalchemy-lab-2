from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    # Customer should exclude reviews.customer
    serialize_rules = ('-reviews.customer',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    reviews = db.relationship('Review', back_populates = 'customer')    # Relationship mapping the customer (one) to related reviews (many)

    # Association proxy to get items for this customer through reviews
    items = association_proxy('reviews', 'item',
                              creator = lambda item_obj: Item(item=item_obj))

    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'


class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'

    # Item should exclude reviews.item
    serialize_rules = ('-reviews.item',) 

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)

    reviews = db.relationship('Review', back_populates = 'item') # Relationship mapping the item(one) to related reviews

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'


class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    # Review should exclude customer.reviews and item.reviews
    serialize_rules = ('-customer.reviews', '-item.reviews',) 

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))

    customer = db.relationship('Customer', back_populates = 'reviews') # Relationship mapping the reviews (many) to related customer (one)
    item = db.relationship('Item', back_populates = 'reviews') # Relationship mapping the reviews(many) to related item (one)

    def __repr__(self):
        return f'<Review {self.id}, {self.comment}>'
