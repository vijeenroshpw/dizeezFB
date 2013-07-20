from flask import Flask, request, jsonify, url_for, redirect, render_template, session
from flask.views import View
from datetime import datetime
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
from flask.ext.restful import reqparse, abort, Api, Resource

import json, facebook, config, random, sys, urllib

#
# A P P  C O N F I G
#
#-- Fetch necessary app parameters to global scope
APP_SECRET = config.APP_SECRET
AUTH_URL = config.AUTH_URL
APP_ID = config.APP_ID

#-- Global app object
app = Flask(__name__,
            static_url_path = '',
            static_folder = '../web-app',
            template_folder='../web-app' )

#-- Global restful api handle
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = config.CONNECTION_URI
db = SQLAlchemy(app)

#
# U T I L S
#


#
# M O D E L S
#
class QCAssociation(db.Model):
  # Question Choice Association
  id          = db.Column(db.Integer,primary_key = True)
  question_id = db.Column(db.Integer,db.ForeignKey('question.id'))
  choice_id   = db.Column(db.Integer,db.ForeignKey('choice.id'))
  choice      = db.relationship("Choice")

  def __repr__(self):
    return "<Assoc q_id %d : c_id %d>"%(self.question_id, self.choice_id)

class QCATAssociation(db.Model):
  # Category Question Association
  id          = db.Column(db.Integer,primary_key = True)
  category_id = db.Column(db.Integer,db.ForeignKey('category.id'))
  question_id = db.Column(db.Integer,db.ForeignKey('question.id'))
  question    = db.relationship("Question")

  def __repr__(self):
    return "<Accoc cat_id %d : q_id %d >"%(self.category_id, self.question_id)  

class Question(db.Model):
  # Question model
  id          = db.Column(db.Integer, primary_key = True)
  text        = db.Column(db.String(240))
  created     = db.Column(db.DateTime)
  correct_choice_id = db.Column(db.Integer)
        # choices point to QCAssociation objects, while each qca object point to a uniqe choice object (bijection)
        # many to many relation ship via Association Model
  choices     = db.relationship('QCAssociation')

  def __init__(self,text):
    self.text = text

  def __repr__(self):
    return "<Question : %s>"%(self.text)

  def json_view(self):
    return {  'id': self.id,
              'text': self.text,
              'choices': self.get_choice_list() }

  def get_choice_list(self):
    #V: Could you explain what goes on here, this function will start to get more complicated so lets preparea
    #-- Currently this method fetches 
    choice_list = []
    correct = 0
    for i in self.choices:
      choice = i.choice
      if self.correct_choice_id == choice.id :
        correct = 1
      choice_list.append(dict(choice_id = choice.id, 
                              text = choice.text, 
                              correct = correct))
      correct = 0
    return choice_list

class Choice(db.Model):
  id            = db.Column(db.Integer, primary_key = True)
  text          = db.Column(db.String(240))
  created       = db.Column(db.DateTime)

  def __init__(self, disease_name ):
    self.text = disease_name

  def __repr__(self):
    return "<Choice : %s>"%(self.text)

class Category(db.Model):
  id            = db.Column(db.Integer, primary_key = True)
  text          = db.Column(db.String(240))
  created       = db.Column(db.DateTime)
        #point to QCATAssociaton object, while each such object points to a uniqe question object      
        #Many to Many relation on Category , Questions

  questions     = db.relationship("QCATAssociation")

  def __repr__(self):
    return "<Category : %s>"%(self.text)


class Game(db.Model):
  id = db.Column(db.Integer,primary_key = True)
  player_id = db.Column(db.String(30))
  player_name = db.Column(db.String(50))
  start_timestamp = db.Column(db.DateTime)
  category = db.Column(db.Integer)
  questions = db.Column(db.String(100))
  num_questions = db.Column(db.Integer)
  user_agent = db.Column(db.String(150))
  player_ip = db.Column(db.String(30))
  
  logs = db.relationship('Log', backref = 'parentGame')

  def __init__(self,player_id = -1, player_name = "Anonymous", category=-1, questions="", num_question=-1,ua="",pip=""):
    self.player_id = player_id
    self.player_name = player_name
    self.category = category
    self.questions = questions
    self.num_questions = num_question
    self.start_timestamp = datetime.now()
    self.user_agent = ua
    self.player_ip = pip

  def __repr__(self):
    return "<game %d , Plaer %s>"%(self.id, self.player_name)



class Log(db.Model):
  id = db.Column(db.Integer,primary_key = True)
  choice_id = db.Column(db.Integer)
  choice_text = db.Column(db.String(100))
  parent_question = db.Column(db.Integer)
  correct = db.Column(db.Integer)
  timestamp = db.Column(db.DateTime)
  game_id = db.Column(db.Integer,db.ForeignKey('game.id'))

  def __init__(self,choice_id = -1, choice_text = "foo", parent_question = -1, correct = 0, game_id = -1):
    self.choice_id = choice_id
    self.choice_text = choice_text
    self.parent_question = parent_question
    self.correct = correct
    self.game_id = game_id
    self.timestamp = datetime.now()
 
  def __repr__(self):
    return "<log_id %d, game_id %d , choice_id %d>"%(self.id,self.game_id,self.choice_id)

  
#
#  A P I
#

class Questions(Resource):
  '''
    GET: Returns list of questions

  '''
  def get(self):
    
    if  session.get('game_id'):              
      category = Category.query.get(session['category'])
      questions = [ qcassoc.question for qcassoc in category.questions ]
      random.shuffle(questions)
      questions = questions[0:session['num_question']]
      
      #-- update the questions field of the game
      game = Game.query.get(session['game_id'])
      game.questions = repr([ q.id for q in questions ])    #-- a simple eval() will result in list revoked
      db.session.commit() 
      
      return [ i.json_view() for i in questions ]
    else:
      questions = Question.query.all()
      return [i.json_view() for i in questions]

class Choices(Resource):
  '''
    POST: writes the log component 
  '''
  def post(self):
    data =  json.loads(request.data)
    log  = Log(data['choice_id'],data['text'],data['parentQuestion'],data['correct'],session['game_id'])
    db.session.add(log)
    db.session.commit()

    
#-- Config API urls
api.add_resource(Questions, '/api/v1/questions')
api.add_resource(Choices,'/api/v1/choices')



#
# Main App Center
#

#-- Routes 
@app.route('/',methods=['GET','POST'])
def index():
  print request.environ 
  #-- each game have a ID , a player id , player name,
  #-- TODO player_id, player_name should be obtained from parsing the signed_request sent by facebook 

  #number of categories
  num_category = len(Category.query.all())
  
  #select a category at random
  category = random.randint(1,num_category)
  
  #number of questions in that category,currently all questions in that category is selected 
  num_question = len(Category.query.get(category).questions)

  game = Game(1,"vijeen",category,"",num_question,request.environ['HTTP_USER_AGENT'],request.environ['REMOTE_ADDR'])
  db.session.add(game)
  db.session.commit()
  
  #populate session so that api can make use of them
  session['game_id'] = game.id 
  session['category'] = category
  session['num_question'] = num_question

  return render_template('index.html')

# Create DB
db.create_all()

if __name__ == '__main__':
    app.debug = True
    app.secret_key = " A big secret key "
    app.run()
