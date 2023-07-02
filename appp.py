from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'  # Database URI
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Define the database model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    college = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    gender = db.Column(db.String(10), nullable=False)
    course = db.Column(db.String(50), nullable=False)
    gpa = db.Column(db.Float, nullable=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the form data
        name = request.form['name']
        college = request.form['college']
        phone = request.form['phone']
        gender = request.form['gender']
        course = request.form['course']
        gpa = float(request.form['gpa'])

        # Check if the student already exists in the database
        existing_student = Student.query.filter_by(name=name, college=college, phone=phone, gender=gender, course=course, gpa=gpa).first()
        if existing_student:
            return "Student already exists in the database."

        # Create a new Student object and add it to the database
        student = Student(name=name, college=college, phone=phone, gender=gender, course=course, gpa=gpa)
        db.session.add(student)
        db.session.commit()

        return redirect('/students')

    return render_template('index.html')

@app.route('/students')
def students():
    # Retrieve all the students from the database
    students = Student.query.all()
    return render_template('students.html', students=students)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the database tables
    app.run(debug=True)


