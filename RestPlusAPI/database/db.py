from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def add(product):  # Type: Product
    db.session.add(product)
    db.session.commit()


def reset():
    db.drop_all()
    db.create_all()

