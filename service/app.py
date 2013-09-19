from flask import Flask, request, jsonify, url_for, redirect, render_template, session
from flask.views import View
from datetime import datetime
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
from flask.ext.restful import reqparse, abort, Api, Resource
import base64,hashlib
import json, facebook, config, random, sys, urllib
from flask.ext.admin import Admin, BaseView, expose
from flask.ext import admin
from flask.ext.admin.contrib.sqlamodel import ModelView
from flask.ext.admin.actions import action
import urllib, urllib2
#
# A P P  C O N F I G
#

#-- Fetch necessary app parameters to global scope

APP_SECRET = config.APP_SECRET
AUTH_URL = config.AUTH_URL
APP_ID = config.APP_ID
ADMINPASS = config.ADMINPASS
ACCESS_TOKEN = config.ACCESS_TOKEN
ACHIEVEMENT_DOMAIN = config.ACHIEVEMENT_DOMAIN

#-- Global app object
app = Flask(__name__,
            static_url_path = '',
            static_folder = '../web-app',
            template_folder='../web-app' )

#-- Admin Handle
class AdminHomeView(admin.AdminIndexView):

  @expose('/',methods=['GET','POST'])
  def index(self):
    questions = len(Question.query.all())
    categories = len(Category.query.all())
    choices = len(Choice.query.all())
    games = len(Game.query.all())

    if request.method =='GET':
      if not session.get('admin'):
        return render_template('adminlogin.html')
      else:
        return self.render('adminhome.html', questions = questions,categories = categories,choices = choices,games=games)
    else:
      passphrase = request.form.get('passphrase')
      print passphrase
      if passphrase == ADMINPASS:
        session['admin'] = True
        #-- redirect to /admin/
        print "Admin Redirect"
        return redirect('/admin/')
      else:
        return render_template('adminlogin.html')



admin = Admin(app ,index_view = AdminHomeView())

#-- Global restful api handle
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = config.CONNECTION_URI
app.secret_key = 'a big secret key'
db = SQLAlchemy(app)

#
# U T I L S
#

def get_questions(api_key='',method=1):
  ''' Accepts api_key and a paramteter method. Method
      determines the criteria by which the questions
      are generated.Currently only one method is de-
      fined. "1 Random Question Selection"
  '''
  #-- Selects 1000 questions at random
  if method ==1:
    questions = Question.query.order_by(func.random()).limit(100).all()
    #questions = questions[1:100]
    return (questions,1)
  #-- Action corresponding to method 2
  elif method == 2:
  #  pass
    questions = []    
    for c in Category.query.all():
      question_list = c.questions
      random.shuffle(question_list)
      if len(question_list) > 30 :
        question_list = question_list[0:30]
      for q in question_list:
        questions.append(q.question)
    return (questions,2)
  #-- Action corresponding to method 3 etc,

  elif method == 3:
    pass

  else:
    pass

def create_if_not_choice(choice_text=""):
  '''
      if this choice do exist ,return its id, else
      create that choice and return its id
  '''
  choice = Choice.query.filter_by(text = choice_text).all()
  if not choice:
    c = Choice(choice_text)
    db.session.add(c)
    db.session.commit()
    return c.id
  else:
    return choice[0].id

def create_if_not_category(category_text = ""):
  '''
      if this categor do exist, return its id ,else
      create it and return its id
  '''
  category = Category.query.filter_by(text = category_text).all()
  if not category:
    c = Category(category_text)
    db.session.add(c)
    db.session.commit()
    return c.id
  else:
    return category[0].id
#
# M O D E L S
#

class QCAssociation(db.Model):
  #-- Question Choice Association
  id          = db.Column(db.Integer,primary_key = True)
  question_id = db.Column(db.Integer,db.ForeignKey('question.id'))
  choice_id   = db.Column(db.Integer,db.ForeignKey('choice.id'))
  choice      = db.relationship("Choice")

  def __repr__(self):
    return "<Assoc q_id %d : c_id %d>"%(self.question_id, self.choice_id)


class QCATAssociation(db.Model):
  #-- Category Question Association
  id          = db.Column(db.Integer,primary_key = True)
  category_id = db.Column(db.Integer,db.ForeignKey('category.id'))
  question_id = db.Column(db.Integer,db.ForeignKey('question.id'))
  question    = db.relationship("Question")

  def __repr__(self):
    return "<Accoc cat_id %d : q_id %d >"%(self.category_id, self.question_id)

class GQAssociation(db.Model):
  #-- Game Question Association
  id = db.Column(db.Integer,primary_key = True)
  game_id = db.Column(db.Integer,db.ForeignKey('game.id'))
  question_id = db.Column(db.Integer,db.ForeignKey('question.id'))
  question = db.relationship("Question")

class Question(db.Model):
  #-- Question model
  id          = db.Column(db.Integer, primary_key = True)
  text        = db.Column(db.String(240))
  created     = db.Column(db.DateTime)
  correct_choice_id = db.Column(db.Integer)
        # choices point to QCAssociation objects, while each qca object point to a uniqe choice object (bijection)
        # many to many relation ship via Association Model
  choices     = db.relationship('QCAssociation')

  def __init__(self,text):
    self.text = text
    self.created = datetime.now()

  def __repr__(self):
    return "<Question : %s>"%(self.text)

  def json_view(self):
    return {  'id': self.id,
              'text': self.text,
              'categories':[ c.category_id for c in QCATAssociation.query.filter_by(question_id=self.id).all() ],
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
    random.shuffle(choice_list)           #-- shuffles the choices , important
    return choice_list

class Choice(db.Model):
  id            = db.Column(db.Integer, primary_key = True)
  text          = db.Column(db.String(240))
  created       = db.Column(db.DateTime)

  def __init__(self, disease_name ):
    self.text = disease_name
    self.created = datetime.now()

  def __repr__(self):
    return "<Choice : %s>"%(self.text)

class Category(db.Model):
  id            = db.Column(db.Integer, primary_key = True)
  text          = db.Column(db.String(240))
  created       = db.Column(db.DateTime)
        #point to QCATAssociaton object, while each such object points to a uniqe question object
        #Many to Many relation on Category , Questions

  questions     = db.relationship("QCATAssociation")

  def __init__(self,ctext):
    self.text  = ctext
    self.created = datetime.now()

  def __repr__(self):
    return "<Category : %s>"%(self.text)


class User(db.Model):
  id          = db.Column(db.Integer,primary_key = True)
  fb_id       = db.Column(db.String(100))
  name        = db.Column(db.String(100))
  api_key     = db.Column(db.Text)
  level       = db.Column(db.Integer,default = 1)

  def __init__(self,name = "",api_key = "",fb_id = ""):
    self.name = name
    self.api_key = api_key
    self.fb_id = fb_id

  def __repr__(self):
    return "<%s>"%(self.name)

  def json_view(self):
    return { 'id'     :self.fb_id,
             'name'   :self.name,
             'api_key':self.api_key,
              'level':self.level }



class Game(db.Model):
  id = db.Column(db.Integer,primary_key = True)
  player_id = db.Column(db.String(30))
  player_name = db.Column(db.String(50))
  start_timestamp = db.Column(db.DateTime)
  category = db.Column(db.Integer)
  questions = db.relationship("GQAssociation")
  num_questions = db.Column(db.Integer)
  user_agent = db.Column(db.String(150))
  player_ip = db.Column(db.String(30))

  logs = db.relationship('Log', backref = 'parentGame')

  def __init__(self,player_id = -1, player_name = "Anonymous", category=-1, num_question=-1,ua="",pip=""):
    self.player_id = player_id
    self.player_name = player_name
    self.category = category
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
quest_parser = reqparse.RequestParser()
quest_parser.add_argument('api_key',type=str,location='cookies')

class Questions(Resource):
  '''
    GET: Returns list of questions

  '''
  def get(self):
    args = quest_parser.parse_args()
    user = db.session.query(User).filter_by(api_key=args['api_key']).first()
    if not user:
      return {'error':'not authenticated'},200
    else:
      env =  request.environ
      #category_count = len(Category.query.all())     #-- number of categories
      #category = random.randint(1,category_count)    #-- selects a category at random
      #question_count = len(Category.query.get(category).questions)  #-- number of questions belonging to that category

      #category = random.choice(Category.query.all())   #-- choose a category at random
      #question_count = len(category.questions)

      #Currently method 1 is used. Later a selection process can be implemented
      questions,method = get_questions(args['api_key'],2)         #Previously it was method 1
      question_count = len(questions)
      #if question_count > 10:          # 10 is given for testing purpose
      #  question_count = 10            # if its < 10 will not alter it.

      #category_instance = Category.query.get(category)  #-- selects category instance
      #questions = [ qcassoc.question for qcassoc in category.questions ]      #-- set of question instances
      #random.shuffle(questions)              #-- shuffles the questions inplace

      #game = Game(user.id,user.name,category.id,question_count,env.get('HTTP_USER_AGENT'),env.get('REMOTE_ADDR'))

      game = Game(user.id,user.name,method,question_count,env.get('HTTP_USER_AGENT'),env.get('REMOTE_ADDR'))


      #game.questions = repr([ q.id for q in questions ])
      db.session.add(game)
      db.session.commit()

      # Now Populate GQAssociation table
      for quest in questions[0:question_count] :
        gqassoc = GQAssociation()
        gqassoc.game_id = game.id
        gqassoc.question_id = quest.id
        db.session.add(gqassoc)

      db.session.commit()

      #populate session with needed informations
      session['game_id'] = game.id


      return [i.json_view() for i in questions[0:question_count] ]

class Choices(Resource):
  '''
    POST: writes the log component
  '''
  def post(self):
    data =  json.loads(request.data)
    log  = Log(data['choice_id'],data['text'],data['parentQuestion'],data['correct'],session['game_id'])
    db.session.add(log)
    db.session.commit()


catquest_parser = reqparse.RequestParser()
catquest_parser.add_argument('category',type=str,location='json')
catquest_parser.add_argument('questions',type=str,location='json')

class NewCategoryQuestion(Resource):
  def put(self,**kwargs):
    args = catquest_parser.parse_args()
    catid = Category.query.filter_by(text=args['category']).all()[0].id
    for quest in eval(args['questions']):
      questions =  Question.query.filter_by(text=quest).all()
      for q in questions:
        qcat = QCATAssociation()
        qcat.question_id = q.id
        qcat.category_id = catid
        db.session.add(qcat)
      db.session.commit()



question_parser = reqparse.RequestParser()
question_parser.add_argument('categories',type=str,location='json')
question_parser.add_argument('choices',type=str,location='json')
question_parser.add_argument('quest_text',type=str,location='json')
question_parser.add_argument('correct_choice',type=int,location='json')


#-- Adds a new question. Backend of /addquest

class NewQuestion(Resource):
  def put(self,**kwargs):
    args = question_parser.parse_args()
    choice_ids = []
    category_ids = []
    #-- gets the choice ids (non existent choice will be created)
    for choice_text in eval(args['choices']):
      print choice_text
      choice_ids.append(create_if_not_choice(choice_text))
    print choice_ids
    #-- gets the cateogory ids (non existent category will be created)
    for category_text in eval(args['categories']):
      print category_text
      category_ids.append(create_if_not_category(category_text))
    print category_ids
    q = Question(args['quest_text'])
    q.correct_choice_id = choice_ids[args['correct_choice']]

    db.session.add(q)
    db.session.commit()

    for choice_id in choice_ids:
      qc = QCAssociation()
      qc.question_id = q.id
      qc.choice_id = choice_id
      db.session.add(qc)
    db.session.commit()

    for category_id in category_ids:
      qcat = QCATAssociation()
      qcat.category_id = category_id
      qcat.question_id = q.id
      db.session.add(qcat)
    db.session.commit()

    return "OK",200




user_parser = reqparse.RequestParser()
user_parser.add_argument('name',type=str,location='json')
user_parser.add_argument('api_key',type=str, location='cookies')
user_parser.add_argument('id',type=str,location='json')
class Users(Resource):
  def get(self,**kwargs):
    args = user_parser.parse_args()
    user = db.session.query(User).filter_by(api_key = args['api_key']).first()
    if not user:
      return {'error':'no_user'},200
    else:
      return user.json_view(),200

  def put(self, **kwargs):
    args = user_parser.parse_args()
    user = db.session.query(User).filter_by(fb_id = args['id']).first()
    if not user:
      new_user = User(args['name'],
                       base64.b64encode(hashlib.sha256( str(random.getrandbits(256)) ).digest(), random.choice(['rA','aZ','gQ','hH','hG','aR','DD'])).rstrip('=='),fb_id = args['id'])
      print args['name'],args['id']      #-- debug
      db.session.add(new_user)
      db.session.commit()
      return new_user.json_view(),200
    else:
      return user.json_view(),200

#-- Config API urls
api.add_resource(Questions, '/api/v1/questions')
api.add_resource(Choices,'/api/v1/choices')
api.add_resource(Users,'/api/v1/user')
api.add_resource(NewQuestion,'/newquestion')
api.add_resource(NewCategoryQuestion,'/newcategoryquestion')


class AddQuestionView(BaseView):
  def is_accessible(self):
    return session.get('admin')

  @expose('/')
  def index(self):
    return self.render('addquest.html')

class LogoutView(BaseView):
  @expose('/')
  def logout(self):
    session.pop('admin')
    return redirect('/admin')

class QuestionAdmin(ModelView):

  column_list = ['text']
  column_searchable_list = ['text']

  def is_accessible(self):
    return session.get('admin')

  @action('remove', 'Remove', 'Are you sure you want to purge  selected models premenantly?')
  def action_merge(self, ids):
    for i in ids:
      qcassocs = QCAssociation.query.filter_by(question_id = i)
      for qcassoc in qcassocs:
        db.session.delete(qcassoc)
      db.session.commit()
      qcatassocs = QCATAssociation.query.filter_by(question_id = i)
      for qcatassoc in qcatassocs:
        db.session.delete(qcatassoc)
      db.session.commit()
      question = Question.query.get(i)
      db.session.delete(question)
      db.session.commit()

class CategoryAdmin(ModelView):

 column_list = ['text']
 column_searchable_list = ['text']

 def is_accessible(self):
   return session.get('admin')

 @action('remove', 'Remove', 'Are you sure you want to purge  selected models premenantly?')
 def action_merge(self, ids):
   for i in ids:
     qcatassocs = QCATAssociation.query.filter_by(category_id = i)
     for qcatassoc in qcatassocs:
       db.session.delete(qcatassoc)
     db.session.commit()
     category = Category.query.get(i)
     db.session.delete(category)
     db.session.commit()



admin.add_view(QuestionAdmin(Question, db.session))
admin.add_view(ModelView(Choice, db.session))
admin.add_view(CategoryAdmin(Category, db.session))
admin.add_view(AddQuestionView(name='Add Question'))
admin.add_view(LogoutView(name="Logout"))

#
# Main App Center
#

#-- Routes
@app.route('/play',methods=['GET','POST'])
def index():
  api_key=request.cookies.get('api_key')
  user = User.query.filter_by(api_key = api_key)[0]
  category_dict = {}
  
  for c in Category.query.all():
    category_dict[c.id] = c.text

  categorylist = json.dumps(category_dict)
  
  if user.name == "Anonymous":
    level = int(request.cookies.get('level'))
    return render_template('play.html',categories=Category.query.all(),levels=range(level,0,-1),fb_id=user.fb_id,user_name=user.name,latest_level = level,app_id = APP_ID,category_dict = categorylist)
  else:
    return render_template('play.html',categories=Category.query.all(),levels=range(user.level,0,-1),fb_id=user.fb_id,user_name=user.name,latest_level = user.level,app_id = APP_ID,category_dict = categorylist)



@app.route('/choices',methods=['GET'])
def searchchoice():
  choice_list = []
  choices = Choice.query.filter(Choice.text.like(request.args['choicestr']+'%'))
  for choice in choices:
    choice_list.append(choice.text)
  return json.dumps(choice_list)

@app.route('/categories',methods=['GET','POST'])
def searchcategory():
  category_list = []
  categories = Category.query.filter(Category.text.like(request.args['catstr']+ '%'))
  for category in categories:
    category_list.append(category.text)

  return json.dumps(category_list)

@app.route('/questions',methods=['GET','POST'])
def searchquestion():
  question_list = []
  questions = Question.query.filter(Question.text.like(request.args['qststr'] + '%'))
  for question in questions:
    question_list.append(question.text)
  return json.dumps(question_list)

@app.route('/api/v1/updatelevel',methods=['GET','POST'])
def updatelevel():
  api_key = request.cookies.get('api_key')
  level = int(request.args.get('level'))
  if api_key:
    users = User.query.filter_by(api_key = api_key).all()
    if users:
      user = users[0]
      user.level = level
      db.session.add(user)
      db.session.commit()
      return "200 Ok"
    else:
      return "No such User"
  else:
      return "No such User"
@app.route('/api/v1/updateachievement',methods=['GET','POST'])
def updateachievement():
  api_key = request.cookies.get('api_key')
  new_achievement = request.args.get('achieved')
  print new_achievement
  users = User.query.filter_by(api_key = api_key)
  user = users[0]
  facebook_id = user.fb_id
  url = 'https://graph.facebook.com/' + facebook_id + '/achievements'
  payload = urllib.urlencode({'access_token':ACCESS_TOKEN,
                            'achievement': ACHIEVEMENT_DOMAIN + 'achieves/'+str(new_achievement)})
  req = urllib2.Request(url,payload)
  response = urllib2.urlopen(req)
  return response.read()


@app.route('/',methods=['GET','POST'])
def server_start():
  return render_template('index.html',app_id = APP_ID)
@app.route('/gameplay',methods=['GET','POST'])
def game_play():
  return render_template('gameplay.html')

@app.route('/achieves/<lid>')
def achievements(lid):
  achs = {'1':'Cancer','2':'Metabolism','3':'Immunilogy','4':'Mental Health ','5':'Kineases','6':'Proteases','7':'Transcriptio factors','8':'All rounder '}
  title = achs[lid] + ' Level'
  url = ACHIEVEMENT_DOMAIN + 'achieves/' + lid
  desc = 'Conqured Level %s , %s Category ' %(lid,achs[lid])
  img = ACHIEVEMENT_DOMAIN + 'img/ach' + lid + '.jpeg'
  point = str(int(lid) * 10)
  app_id = APP_ID
  print lid
  return render_template('/ach.html',title = title,url = url,desc = desc,img = img,point = point,app_id = app_id)

# Create DB
def create_db():
  db.create_all()
db.create_all()

if __name__ == '__main__':
    app.debug = True
    app.run()
