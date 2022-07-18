from flask import Flask , render_template , url_for , request , redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)


class ToDo(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    content = db.Column(db.String(200) , nullable = False)
    # completed = db.column(db.Integer , default= 0)
    date_created = db.Column(db.DateTime , default = datetime.utcnow)

    def __repr__(self):
        return 'task %r' % self.id


@app.route('/' , methods=['POST' , 'GET'])
def index():
    if request.method =="POST":
        task_content = request.form['content']
        new_task = ToDo(content = task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "there is issue with your submit"

    else:
        tasks = ToDo.query.order_by(ToDo.date_created).all()
        return render_template('index.html' , tasks = tasks)

@app.route('/delete/<int:id>')
def deleteTask(id):
    task_to_delete = ToDo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'cante delete the task dont know why'

@app.route('/update/<int:id>' , methods=["GET","POST"])
def updateContent(id):
    updated_task = ToDo.query.get_or_404(id)
    if request.method == 'POST':
        updated_task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "there was problem in updating"
    else:
        return render_template('update.html' , task = updated_task)


    




if __name__ =='__main__':
    app.run(debug= True)