from flask import Flask,render_template,request
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
import json
import facebook
import config
import random

APP_SECRET = config.APP_SECRET

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.CONNECTION_URI

db  = SQLAlchemy(app)


class Questions(db.Model):
	id = db.Column(db.Integer,primary_key = True)
	clue_id = db.Column(db.String(20))
	clue_name = db.Column(db.String(20))
	succes_rate = db.Column(db.Integer)
	clue = db.Column(db.String(50))
	answer = db.Column(db.String(50))
	doid = db.Column(db.String(15))
	wrong_diseases = db.Column(db.String(50))
	correct_id = db.Column(db.Integer)
	categories = db.Column(db.String(50))

	def __init__(self, clue_id,clue_name,success_rate,clue,answer,doid,wrong_diseases,correct_id,categories):
		self.clue_id = clue_id
		self.clue_name = clue_name
		self.success_rate = success_rate
		self.clue = clue
		self.answer = answer
		self.doid = doid
		self.wrong_diseases = wrong_diseases
		self.correct_id = correct_id
		self.categories = categories
	
	def __repr__(self):
		return "<Question Clue : %s>"%(self.clue)

class Diseases(db.Model):
	id = db.Column(db.Integer,primary_key = True)
	disease_name  = db.Column(db.String(100))
	def __init__(self,disease_name):
		self.disease_name = disease_name
	def __repr__(self):
		return "<Disease : %s>"%(self.disease_name)


def fetch_questions(category = 0):
	if category == 0:
		results = Questions.query.order_by(func.rand()).limit(50).all()
	else:
		results = Questions.query.filter(Questions.categories.like("%" + str(category) + "%")).order_by(func.rand()).limit(50).all()
	
	quests = []
	for result in results:
		rand_choices = [ int(x) for x in result.wrong_diseases.split("|") ]
		rand_choices.append(result.correct_id)
		random.shuffle(rand_choices)
		quests.append(dict(question_id = result.id,clue_id = result.clue_id,clue_name = result.clue_name,success_rate = result.succes_rate,clue = result.clue,answer = result.answer,doid = result.doid,choice_list = rand_choices,correct_index = rand_choices.index(result.correct_id)))
	return json.dumps(quests)

	
def fetch_diseases():
	results  = Diseases.query.all()
	diseases = []
	for result in results:
		diseases.append(dict(disease_id = result.id,disease_name = result.disease_name))
	return json.dumps(diseases)



@app.route('/',methods=['GET','POST'])
def index():
	return render_template('index.html',auth_url = AUTH_URL)


	
@app.route('/game',methods=['GET','POST'])
def game():
	if request.method == 'POST':
		if 'signed_request' in request.form:
			print " Yes Signed Request obtained"
		else:
			print " No Signed Request Obtained"

		return render_template('game.html')
	else:
		return render_template('game.html')


@app.route('/test',methods=['GET','POST'])
def test():
	return 	render_template('test.html')


@app.route('/questions',methods=['GET','POST'])
def questions():
	return fetch_questions()


@app.route('/diseases',methods=['GET','POST'])
def diseases():	
	return fetch_diseases()

if __name__ == '__main__':
	app.run()


