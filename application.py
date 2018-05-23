from flask import Flask, flash, redirect, url_for, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from kapsch import create_app, db
from io import BytesIO
import base64
from PIL import Image




# Configure application
app = Flask(__name__)
app = create_app()

# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


from kapsch.models import Photo , get_image
with app.app_context():
    db.create_all()


@app.route("/", methods=['GET'])
def show_all():
    session["image_id"] = 1
    return render_template('main.html')

@app.route('/image', methods=['GET'])
def get_images_from_db():
    image = get_image(session["image_id"])
    return render_template('main.html', image=image)


@app.route('/image/<int:the_id>', methods=['GET'])
def get_image_from_db(the_id):
    image =get_image(the_id)
    return app.response_class(image.img_data, mimetype='application/octet-stream')


@app.route("/categorize", methods=['POST'])
def categorize():
    image_category = request.form['category']
    image_query = Photo.query.get(session["image_id"])
    image_query.category = image_category
    db.session.commit()
    return render_template('main.html', image=image_query)

@app.route("/bring_next", methods=['GET','POST'])
def bring_next():
        session["image_id"] += 1
        return redirect(url_for('get_images_from_db'))


@app.route("/upload", methods=['POST'])
def upload():
    file = request.files['inputfile']
    newFile = Photo(file.read())
    db.session.add(newFile)
    db.session.commit()
    return render_template('main.html')










