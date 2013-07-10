from flask import Flask,render_template,request
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
from flask.ext.restful import Resource, Api

import json, facebook, config, random, sys, urllib

#-- fetch necessary app parameters to global scope 
APP_SECRET = config.APP_SECRET
AUTH_URL = config.AUTH_URL
APP_ID = config.APP_ID

#-- global app object
app = Flask(__name__)

#-  connection url , specifying location, port , username , password , dbname 
app.config['SQLALCHEMY_DATABASE_URI'] = config.CONNECTION_URI

#-- Global database handle
db  = SQLAlchemy(app)

#-- Global restful api handle
api = Api(app)

#
# M O D E L S
#
class Question(db.Model):
  id              = db.Column(db.Integer,primary_key = True)
  clue_id         = db.Column(db.String(20))
  clue_name       = db.Column(db.String(20))
  succes_rate     = db.Column(db.Integer)
  clue            = db.Column(db.String(50))
  answer          = db.Column(db.String(50))
  doid            = db.Column(db.String(15))
  wrong_diseases  = db.Column(db.String(50))
  correct_id      = db.Column(db.Integer)
  categories      = db.Column(db.String(50))

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

class Disease(db.Model):
  id            = db.Column(db.Integer,primary_key = True)
  disease_name  = db.Column(db.String(100))

  def __init__(self,disease_name):
    self.disease_name = disease_name

  def __repr__(self):
    return "<Disease : %s>"%(self.disease_name)

#
# A P I
#



#-- Questions Resource ,    /api/v1/questions/1 returns list of questions (in JSON) questin belong to category 1
class QuestionsResource(Resource):
  def get(self,category):
    return fetch_questions(int(category))
    
#-- Diseases Resource     /api/v1/diseases  returns list of all diseases (in JSON)
class DiseasesResource(Resource):
  def get(self):
    return fetch_diseases()

#-- /api/v1/questchoice/<category>/<num_choices> returns questions of category , with num_choice choices
class QuestChoiceResource(Resource):
  def get(self,category,num_choices):
    return fetch_questchoice(int(category),int(num_choices))
    

#-- Configuring api urls
api.add_resource(QuestionsResource,'/api/v1/questions/<string:category>')
api.add_resource(DiseasesResource,'/api/v1/diseases')
api.add_resource(QuestChoiceResource,'/api/v1/questchoice/<string:category>/<string:num_choices>')


#-- Fetches questions of given category
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
  return quests

#-- Fetches all diseases
def fetch_diseases():
  results  = Diseases.query.all()
  diseases = []
  for result in results:
    diseases.append(dict(disease_id = result.id,disease_name = result.disease_name))
  return diseases



#-- Returns a random list of  n diseases,including the correct_disease index
def fetch_choices(correct_choice,num_choice):
  rand_list = []
  while len(rand_list) != (num_choice-1) :
    rand_num = random.randint(1,836)
    if rand_num not in rand_list:
      if rand_num != correct_choice:
        rand_list.append(rand_num)
  rand_list.append(correct_choice)
  random.shuffle(rand_list)
  #-- the location of correct ID
  correct_id = rand_list.index(correct_choice)
  rand_choices = []
  for i in rand_list:
    disease = Diseases.query.get(i)
    rand_choices.append(dict(disease_id=disease.id,disease_name=disease.disease_name))
  return (rand_choices,correct_id)
  


##-- Fetches questions of given category, along with "num_choices", returns a list of diseases , id of correct disease
def fetch_questchoice(category=0,num_choices = 3):
  if category == 0:
    results = Questions.query.order_by(func.rand()).limit(50).all()
  else:
    results = Questions.query.filter(Questions.categories.like("%" + str(category) + "%")).order_by(func.rand()).limit(50).all()

  quests = []
  for result in results:
    choice_list,correct_id = fetch_choices(result.correct_id + 1,num_choices)
    quests.append(dict(question_id = result.id,clue_id = result.clue_id,clue_name = result.clue_name,success_rate = result.succes_rate,clue = result.clue,answer = result.answer,doid = result.doid,choices_collection = choice_list,correct_index = correct_id))
  return quests

@app.route('/',methods=['GET','POST'])
def index():
  return render_template('index.html',auth_url = AUTH_URL)

@app.route('/game',methods=['GET','POST'])
def game():
  if request.method == 'POST':
    if 'signed_request' in request.form:
      print " Yes Signed Request obtained"

      #parsing signed request obtained
      sr_data = facebook.parse_signed_request(request.form['signed_request'],APP_SECRET)
      #getting the graph object
      graph = facebook.GraphAPI(sr_data['oauth_token'])
      #obtains self profile
      profile = graph.get_object("me")
      #gets list of my frineds
      friends = graph.get_connections("me","friends")
      #gets the list of players who plays this game + score
      scores = graph.get_object("/"+APP_ID+"/scores")
      print scores
      for player in scores['data']:
        print player['user']['name'],player['score'],player['user']['id']

      try:
        #stuff = graph.get_object("https://graph.facebook.com/me/picture",redirect=False)
              stuff = urllib.urlopen("https://graph.facebook.com/me/picture?redirect=false&access_token="+sr_data['oauth_token'])
          
        print stuff.read()
      except:
        print sys.exc_info()

      #Homework to be done 
                           #1 getting profile pics of friends
    else:
      print " No Signed Request Obtained"

    return render_template('game.html')
  else:
    return render_template('game.html')


@app.route('/play/<category>',methods=['GET','POST'])
def mtest(category=0):
  return render_template('app.html',fetch_url = '/api/v1/questions/'+category)

if __name__ == '__main__':
  app.run(debug=True)
