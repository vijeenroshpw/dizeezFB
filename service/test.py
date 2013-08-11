import os
import app
import unittest
import tempfile
import json
from flask.ext.sqlalchemy import SQLAlchemy

app.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.app.config['TESTING'] = True

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
	''' Sets up the testing environment 
            adds a single category and a single question to it '''
        self.test_client = app.app.test_client()
        app.create_db()
        quest = app.Question("Test Question")
        category = app.Category("Test Category")
        
        app.db.session.add(quest)
        app.db.session.add(category)
        app.db.session.commit()
        qcatassoc = app.QCATAssociation()
        qcatassoc.category_id = quest.id
        qcatassoc.question_id = category.id
        app.db.session.add(qcatassoc)
        app.db.session.commit()
       
    def tearDown(self):
	''' Destroys the testing environment '''
    
    def test_user_management(self):
	''' Tests the User Management Functionality '''
 	
        self.response = ''
        json_data = json.dumps(dict(id='12345',name='testuser'))
        
        #-- CREATE A NEW USER --#
        print "Creating New User"
        self.response = self.test_client.put('/api/v1/user',data = json_data,content_type='application/json').data
        assert "12345" in self.response and 'testuser' in self.response
        print "Success !!!" 
          
        #save the api_key obtained 
        self.api_key = json.loads(self.response)['api_key']
       	#print self.api_key 
        
        #-- RECREATE Same user again to see if duplicate entery occurs --#
        print "RECREATING same (user Duplication Test) "
        self.response = self.test_client.put('/api/v1/user',data = json_data,content_type='application/json').data
        assert json.loads(self.response)['api_key'] == self.api_key
	print "Success !!!"

        #-- Tests whether GET to /api/v1/user returns correct user details if a valid cookie exists --#
        print "Testing GET /api/v1/user"
        self.response = self.test_client.get('/api/v1/user', headers=[('Cookie', 'api_key='+self.api_key)]).data
        assert "12345" in self.response
        print "Success !!!"

	#-- Test if Questions are correctly rendered in case of a valid api_key --#        
        print "Testing GET /api/v1/question "
        self.response = self.test_client.get('/api/v1/questions', headers=[('Cookie', 'api_key='+ self.api_key)]).data
        assert 'Test Question' in  self.response
        print "Success !!!"

        os.remove('/tmp/test.db')

if __name__ == '__main__':
    unittest.main()
