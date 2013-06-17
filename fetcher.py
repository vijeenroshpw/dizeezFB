import MySQLdb
import json
import random
import config

DBUSER = config.USERNAME
DBPASS = config.PASSWORD
DBNAME = config.DBNAME
DBHOST = config.DBHOST

def getQuestions(category = 0):
	db = MySQLdb.connect(DBHOST,DBUSER,DBPASS,DBNAME)
	cursor = db.cursor()
	cursor.execute("SELECT * FROM Questions ORDER BY RAND() LIMIT 0,50")
	results = cursor.fetchall()
	quests = []
	for result in results:
		rand_choices = [ int(x) for x in result[7].split('|') ]
		rand_choices.append(result[8])
		random.shuffle(rand_choices)
		
		quests.append(dict(question_id = result[0],clue_id=result[1],clue_name=result[2],succes_rate=result[3],clue=result[4],answer=result[5],doid=result[6],choice_list = rand_choices,correct_index=rand_choices.index(result[8])))
	
	db.close()
	return  json.dumps(quests)

def getDiseases():
	db = MySQLdb.connect(DBHOST,DBUSER,DBPASS,DBNAME)
	cursor = db.cursor()
	cursor.execute("SELECT * FROM Diseases ")
	results = cursor.fetchall()
	quests = []
	for result in results:
		quests.append(dict(disease_id = result[0],disease_name = result[1]))
	db.close()			
	return json.dumps(quests)


