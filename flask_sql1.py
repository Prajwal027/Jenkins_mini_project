from flask import Flask, render_template, url_for, request, redirect
import os
app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
#db.init_app(app)
class student(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(100), nullable = False)
    lastname = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), unique = True, nullable = False)
    age = db.Column(db.Integer)
    time = db.Column(db.DateTime(timezone=True), server_default = func.now())
    bio = db.Column(db.Text)

    def __repr__(self):
        return f"<student {self.firstname}>"

@app.route('/')
def index():
    students = student.query.all()
    return render_template('index.html', students=students)
@app.route('/<int:S_id>')
def stud(S_id):
    student1 = student.query.get_or_404(S_id)
    return render_template('student.html', student=student1)

@app.route('/create', methods=('POST','GET'))
def create():
    if request.method=='POST':
        firstname1=request.form['firstname']
        lastname=request.form['lastname']
        email=request.form['email']
        age=int(request.form['age'])
        bio=request.form['bio']
        firstname1 = student(firstname=firstname1, lastname=lastname, email=email, age=age, bio=bio)
        db.session.add(firstname1)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/<int:S_id>/edit', methods=('POST', 'GET'))
def edit(S_id):
    student2 = student.query.get_or_404(S_id)
    
    if request.method=='POST':
        firstname=request.form['firstname']
        lastname=request.form['lastname']
        email=request.form['email']
        age=int(request.form['age'])
        bio=request.form['bio']

        student2.firstname=firstname
        student2.lastname=lastname
        student2.email=email
        student2.age=age
        student2.bio=bio

        db.session.add(student2)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('create.html', student=student2)

@app.post('/<int:S_id>/delete')
def delete(S_id):
    student3 = student.query.get_or_404(S_id)
    db.session.delete(student3)
    db.session.commit()
    return redirect(url_for('index'))

if __name__=='__main__':
    app.run(debug=True)

