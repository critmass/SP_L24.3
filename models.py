"""Models for Cupcake app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFUALT_IMAGE_URL = "https://tinyurl.com/demo-cupcake"

def connect_db(app):
    # this was lifted from the wabbler project
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)


class Cupcake( db.Model ):

    __tablename__ = 'cupcakes'

    # id: a unique primary key that is an auto-incrementing integer
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    # flavor: a not-nullable text column
    flavor = db.Column(
        db.Text,
        nullable = False
    )

    # size: a not-nullable text column
    size = db.Column(
        db.Text,
        nullable = False
    )

    # rating: a not-nullable column that is a float
    rating = db.Column(
        db.Float,
        nullable = False
    )

    # image: a non-nullable text column. If an image is not given, default to https://tinyurl.com/demo-cupcake
    image = db.Column(
        db.Text,
        default = DEFUALT_IMAGE_URL
    )

    # serialize: this method is used to serialize cupcakes for use with json
    @classmethod
    def serialize( cls, cupcake ):
        return {
            "id": cupcake.id,
            "flavor": cupcake.flavor,
            "size": cupcake.size,
            "rating": cupcake.rating,
            "image": cupcake.image
        }