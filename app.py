from flask import Flask, url_for, render_template, redirect, flash

from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Pet
from forms import AddPet, EditPet

app = Flask(__name__)

app.config['SECRET_KEY'] = "supersecretsecrets"

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///adopt"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

with app.app_context():
    connect_db(app)
    db.create_all()

    toolbar = DebugToolbarExtension(app)


@app.route("/")
def pets_list():
    """Shows a list of all current pets"""
    pets = Pet.query.all()
    return render_template("pets.html", pets=pets)


@app.route("/add", methods=["GET", "POST"])
def add_pet():
    """Takes user to AddPet Form"""
    form = AddPet()

    if form.validate_on_submit():
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        new_pet = Pet(**data)
        
        db.session.add(new_pet)
        db.session.commit()

        flash(f"{new_pet.name} added.")

        return redirect(url_for('pets'))

    else:
        return render_template("pets_add.html", form=form)


@app.route("/<int:pet_id>", methods=["GET", "POST"])
def edit_pet(pet_id):
    """Takes user to EditPet form"""

    pet = Pet.query.get_or_404(pet_id)
    form = EditPet(obj=pet)

    if form.validate_on_submit():
        pet.notes = form.notes.data
        pet.available = form.available.data
        pet.photo_url = form.photo_url.data
        db.session.commit()

        flash(f"{pet.name} updated.")

        return redirect(url_for('pets'))

    else:
        return render_template("pets_edit.html", form=form, pet=pet)


