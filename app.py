from flask import Flask, request, jsonify, url_for, redirect, render_template
from flask.views import View

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
app = Flask(__name__)

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
class Question(db.Model):
  '''
    So this will be the model which repersents a question. A question is simply a string of text
    that can have a doid, it have many categories, and it can have many choices. 1 of the choices
    should be flagged as correct
  '''
  id          = db.Column(db.Integer, primary_key = True)
  text        = db.Column(db.String(240))
  created     = db.Column(db.DateTime)

  categories  = db.relationship('Category', backref=db.backref('question',  lazy='select'))
  choices     = db.relationship('Choice', backref=db.backref('question',  lazy='select'))

  def __init__(self,text):
	self.text = text

  def __repr__(self):
    return "<Question : %s>"%(self.text)

  def json_view(self):
    # This gets the relationship of all the child choices
    print self.choices
    return {  'id'          : self.id,
              'text'        : self.text,
              'choices'     : [ dict(text=c.text,correct = c.correct,question_id = c.question_id) for c in self.choices ] }

class Choice(db.Model):
  '''
    A choice is a potential answer to a question. A question can have unlimited choices. A question
    must have at least 1 choice that is flagged as correct
  '''
  id            = db.Column(db.Integer, primary_key = True)
  text          = db.Column(db.String(240))
  created       = db.Column(db.DateTime)
  correct       = db.Column(db.Integer)
  question_id   = db.Column(db.Integer, db.ForeignKey('question.id'))

  def __init__(self, disease_name,question_id ,correct = 0 ):
    self.text = disease_name
    # @V Why might this be a bad idea or something that prevents the extexibility of using choices?
    # Could a choice be the correct choice for more than 1 question? How do we prevent 2 identical choices 
    # from appearing in the DB more than once whose only difference is the Choice.correct Bool
    self.correct = correct
    self.question_id = question_id

  def __repr__(self):
    return "<Choice : %s>"%(self.text)

class Category(db.Model):
  id            = db.Column(db.Integer, primary_key = True)
  text          = db.Column(db.String(240))
  created       = db.Column(db.DateTime)

  question_id   = db.Column(db.Integer, db.ForeignKey('question.id'))

  def __repr__(self):
    return "<Category : %s>"%(self.text)

#
# A P I
#
class Questions(Resource):
  '''
    GET: Returns list of questions

  '''
  def get(self):
    questions = Question.query.all()
    # @V I put this in here for a reason, the way you replaced it with is 
    # incorrect and a security issue: http://flask.pocoo.org/docs/security/#json-security
    return [i.json_view() for i in questions]
    #return jsonify(objects=[i.json_view() for i in questions])

#-- Config API urls
api.add_resource(Questions, '/api/v1/questions')

#
# Boring old standard routes / need to figure 
# out what importance these actually have?
#
@app.route('/', methods=['GET', 'POST'])
def index():
  return render_template('index.html', auth_url = AUTH_URL)

@app.route('/game', methods=['GET', 'POST'])
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
        stuff = urllib.urlopen("https://graph.facebook.com/me/picture?redirect=false&access_token="+sr_data['oauth_token'])
        print stuff.read()
      except:
        print sys.exc_info()

    else:
      print " No Signed Request Obtained"

    return render_template('game.html')
  else:
    return render_template('game.html')

#
# Main App Center
#

# Create DB
db.create_all()

if __name__ == '__main__':
    app.debug = True
    app.run()
