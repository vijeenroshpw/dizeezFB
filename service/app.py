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
    #V: Could you explain what goes on here, this function will start to get more complicated so lets prepare
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

#
#  A P I
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
# Main App Center
#

# Create DB
db.create_all()

if __name__ == '__main__':
    app.debug = True
    app.run()
