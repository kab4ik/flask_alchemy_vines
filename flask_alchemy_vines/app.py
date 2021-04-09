from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vines.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Vine(db.Model):
    __tablename__ = 'VINES'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float)
    sorted_id = db.Column(db.Integer, db.ForeignKey('SORTS.id'))
    sort = db.relationship('Sort', backref=db.backref('vines'))
    producer_id = db.Column(db.Integer, db.ForeignKey('PRODUCERS.id'))
    producer = db.relationship('Producer', backref=db.backref('vines'))
    def __str__(self):
        return self.name

class Sort(db.Model):
    __tablename__ = 'SORTS'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    def __str__(self):
        return self.name


class Producer(db.Model):
    __tablename__ = 'PRODUCERS'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    def __str__(self):
        return f'\"{self.name}\"'

@app.route('/')
def start():
    return redirect(url_for('index'))

@app.route('/index')
@app.route('/index/<string:sort_type>')
def index(sort_type=None):
    vines = Vine.query.all()
    if sort_type == 'byname':
        vines.sort(key=lambda x: x.name)
    if sort_type == 'bypricelow':
        vines.sort(key=lambda x: x.price)
    if sort_type == 'bypricehigh':
        vines.sort(key=lambda x: -x.price)
    if sort_type == 'byproducer':
        vines.sort(key=lambda x: (x.producer.name, x.name))
    return render_template('index.html', vines=vines)

@app.route('/vine/<int:pk>')
def vine(pk):
    vine = Vine.query.get(pk)
    return render_template('vine.html', vine=vine)

if __name__ == '__main__':
    app.run(debug=True)