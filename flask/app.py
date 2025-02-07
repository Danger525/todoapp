from multiprocessing.resource_tracker import getfd
from flask import Flask, render_template, request, redirect, flash
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    slno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)  # ✅ Fixed default value

    def __repr__(self) -> str:
        return f"{self.slno} - {self.title}"

# Create tables before running the app
with app.app_context():
    db.create_all()

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        title = request.form.get('title')
        desc = request.form.get('desc')

        if title and desc:  # ✅ Ensure values are not empty
            todo = Todo(title=title, desc=desc)  # ✅ Insert user input
            db.session.add(todo)
            db.session.commit()
            return redirect("/")  # ✅ Redirect to avoid form resubmission

    alltodo = Todo.query.all()
    return render_template('index.html', alltodo=alltodo)  # ✅ Always return a response

@app.route("/show")
def products():
    alltodo = Todo.query.all()
    print(alltodo)
    return "This is the product page"

@app.route("/delete/<int:slno>")
def delete(slno):
    guide = Todo.query.get(slno)
    db.session.delete(guide)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:slno>', methods=['GET', 'POST'])
def update(slno):
    todo = Todo.query.get_or_404(slno)  # Get the record or return 404

    if request.method == 'POST':
        todo.title = request.form['title']
        todo.desc = request.form['desc']
        db.session.commit()  # Commit the changes to the database
        return redirect('/')
    return render_template('update.html', todo=todo)

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == '__main__':
    app.run(debug=True)