from flask import Flask, render_template, request
from werkzeug.utils import redirect
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    img_url = db.Column(db.String(300))
    ansA = db.Column(db.String(200), nullable=False)
    ansB = db.Column(db.String(200), nullable=False)
    ansC = db.Column(db.String(200), nullable=False)
    ansD = db.Column(db.String(200), nullable=False)
    cor = db.Column(db.Integer)
    prev_correct = db.Column(db.Integer)
    prev_incorrect = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "Question:" + str(self.id) + " " + self.content

@app.route("/", methods=['GET', 'POST'])
def index():
        quests = Question.query.order_by(Question.date_created).all()
        return render_template("index.html", q=quests)

@app.route('/add/', methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        return render_template("add.html")
    if request.method == 'POST':
       new_question = Question(content=request.form['content'], img_url = request.form['url_img'], ansA=request.form['ans1'], ansB=request.form['ans2'],
                               ansC=request.form['ans3'], ansD=request.form['ans4'], cor=int(request.form['cor']), prev_correct=0, prev_incorrect=0)
       try:
           db.session.add(new_question)
           db.session.commit()
           return redirect("/")
       except:
            return "No dice."

@app.route("/quiz/", methods=['GET', 'POST'])
def quiz():
    ques = Question.query.order_by(sqlalchemy.sql.functions.random()).first()
    result = ""
    if request.method == 'POST':
        q_id = int(request.form['id'])
        q_check = Question.query.get_or_404(q_id)
        ans = request.form['ans']
        if q_check.cor == 1 and ans == "A":
            result = "Correct!"
            q_check.prev_correct += 1
        elif q_check.cor == 2 and ans == "B":
            result = "You got it!"
            q_check.prev_correct += 1
        elif q_check.cor == 3 and ans == "C":
            result = "You got it!"
            q_check.prev_correct += 1
        elif q_check.cor == 4 and ans == "D":
            result = "You got it!"
            q_check.prev_correct += 1
        else:
            result = "Not quite!"
            q_check.prev_incorrect += 1
        db.session.commit()
    return render_template("quiz.html",q = ques, res = result)
