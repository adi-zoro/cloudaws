from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

application = Flask(__name__)

# local dbms config
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost/flaskcloud'
application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:mypassword@mydb.cxhtwibyzspu.eu-west-1.rds.amazonaws.com/flaskcloud'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.secret_key = "pwd123a"

db = SQLAlchemy(application)


# creating table model for our app
class inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float)

    def __init__(self, title, type, price):
        self.title = title
        self.type = type
        self.price = price


@application.route("/")
def index():
    items = inventory.query.all()
    return render_template('index.html', items=items)


@application.route('/add/', methods=['POST'])
def insert_items():
    if request.method == "POST":
        item = inventory(
            title=request.form.get("title"),
            type=request.form.get("type"),
            price=request.form.get("price")

        )
        db.session.add(item)
        db.session.commit()
        flash("Item added Successfully")
        return redirect((url_for('index')))


@application.route('/update/', methods=['POST'])
def update():
    if request.method == "POST":
        my_data = inventory.query.get(request.form.get('id'))
        my_data.title = request.form['title']
        my_data.type = request.form['type']
        my_data.price = request.form['price']

        db.session.commit()
        flash("Item is updated")
        return redirect(url_for('index'))


@application.route('/delete/<id>', methods=['GET', 'POST'])
def delete(id):
    my_data = inventory.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Item is deleted")
    return redirect(url_for('index'))


if __name__ == "__main__":
    application.run(debug=True)
