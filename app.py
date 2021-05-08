"""Flask app for Cupcakes"""
import os

from flask import Flask, request, jsonify, render_template

from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', \
        'postgres://postgres:MTasXgD9@localhost/cupcakes')
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "oh-so-secret"

connect_db(app)

@app.route('/')
def get_page():
    # GET /
    # This should return an HTML page (via render_template). 
    # This page should be entirely static (the route should 
    # just render the template, without providing any information 
    # on cupcakes in the database). It should show simply have an 
    # empty list where cupcakes should appear and a form where new 
    # cupcakes can be added.
    return render_template("home.html")

@app.route('/api/cupcakes', methods=["GET"])
def list_cupcakes():
    # GET /api/cupcakes
    # Get data about all cupcakes.

    # Respond with JSON like: 
    # {cupcakes: [{id, flavor, size, rating, image}, ...]}.

    # The values should come from each cupcake instance.

    cupcakes = Cupcake.query.all()
    serialized_cupcakes = [ Cupcake.serialize( cc ) for cc in cupcakes ]
    return jsonify( cupcakes = serialized_cupcakes )

@app.route('/api/cupcakes/<cupcake_id>', methods=["GET"])
def get_cupcakes( cupcake_id ):
    # GET /api/cupcakes/[cupcake-id]
    # Get data about a single cupcake.

    # Respond with JSON like: {cupcake: {id, flavor, size, rating, image}}.

    # This should raise a 404 if the cupcake cannot be found.

    cupcake = Cupcake.query.get_or_404( cupcake_id )
    serialized_cupcake = Cupcake.serialize( cupcake )

    return jsonify( cupcake = serialized_cupcake )

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    # POST /api/cupcakes
    # Create a cupcake with flavor, size, rating and 
    # image data from the body of the request.

    # Respond with JSON like: {cupcake: {id, flavor, size, rating, image}}.

    flavor = request.json["flavor"]
    size   = request.json["size"]
    rating = request.json["rating"]
    image = None

    try:
        image  = request.json["image"]
    except:
        image = None

    cupcake = Cupcake(
        flavor = flavor,
        size   = size,
        rating = rating,
        image  = image
    )

    db.session.add( cupcake )
    db.session.commit()

    serialized_cupcake = Cupcake.serialize( cupcake )

    return jsonify( cupcake = serialized_cupcake )

@app.route('/api/cupcakes/<cupcake_id>', methods=["PATCH"])
def update_cupcake( cupcake_id ):
    # PATCH /api/cupcakes/[cupcake-id]
    # Update a cupcake with the id passed in the URL and flavor, 
    # size, rating and image data from the body of the request. 
    # You can always assume that the entire cupcake object will 
    # be passed to the backend.

    # This should raise a 404 if the cupcake cannot be found.

    # Respond with JSON of the newly-updated cupcake, like this: {cupcake: {id, flavor, size, rating, image}}.

    cupcake = Cupcake.query.get_or_404( cupcake_id )

    cupcake.flavor = request.json["flavor"]
    cupcake.size   = request.json["size"]
    cupcake.rating = request.json["rating"]
    cupcake.image  = request.json["image"]

    db.session.add( cupcake )
    db.session.commit()

    serialized_cupcake = Cupcake.serialize( cupcake )

    return jsonify( cupcake = serialized_cupcake )

@app.route('/api/cupcakes/<cupcake_id>', methods=["DELETE"])
def remove_cupcake( cupcake_id ):
    # DELETE /api/cupcakes/[cupcake-id]
    # This should raise a 404 if the cupcake cannot be found.

    # Delete cupcake with the id passed in the URL. 
    # Respond with JSON like {message: "Deleted"}.

    cupcake = Cupcake.query.get_or_404( cupcake_id )

    db.session.delete( cupcake )
    db.session.commit()

    return jsonify(message="deleted")
