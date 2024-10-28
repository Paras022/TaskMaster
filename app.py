from flask import Flask , render_template , redirect , request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
import datetime

# my app setup
app = Flask(__name__)
Scss(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db = SQLAlchemy(app)

# data model
class MyTask(db.Model):
    id = db.Column(db.Integer , primary_key=True )
    content = db.Column(db.String(100) ,nullable = False)
    complete = db.Column(db.Integer , default =0)
    created = db.Column(db.DateTime , default= datetime.datetime.now())

    def __repr__(self) -> str:
        return f"Task {self.id}"
    
with  app.app_context():
        db.create_all()

# routes  
@app.route("/" , methods = ["POST" ,"GET"])
def index():
    # add task
    if request.method == "POST":
        current_task =  request.form['content']
        new_task = MyTask(content = current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(f"ERROR:{e}")
            return f"ERROR:{e}"
    else:
        tasks = MyTask.query.order_by(MyTask.created).all()
        return render_template('index.html' ,tasks = tasks)
    

# delete  route for an item
@app.route("/delete/<int:id>/")
def delete(id:int):
    delete_task = MyTask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"ERROR:{e}"

# updating a task
@app.route("/edit/<int:id>/" , methods = ["POST" ,"GET"])
def edit(id:int):
    task = MyTask.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"ERROR:{e}"
    else:
        return render_template('edit.html', task = task)



if __name__ == "__main__":
    
    app.run(debug=True)