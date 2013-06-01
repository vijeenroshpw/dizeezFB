import MySQLdb
import data
import random
game_json = data.games
disease_json = data.diseases


db = MySQLdb.connect('localhost','root','root','dizeeztest')
cursor = db.cursor()

def genRandomSet(maximum=0,disease_id=0):
	random_list = []
	while len(random_list) != 5:
		rand_num = random.randint(0,maximum)
		if rand_num not in random_list:
			if rand_num != disease_id:
				random_list.append(str(rand_num))

	return random_list[0] + "|" + random_list[1] + "|" + random_list[2] + "|" + random_list[3] 


def getDiseaseId(disease_name):
	 cursor.execute('''SELECT * FROM Diseases WHERE disease_name="'''+disease_name+'''";''')
	 return cursor.fetchone()[0]
	 

def loadGeneData():
	id = 0
	temp = '''INSERT INTO Questions VALUES(%d,"%s","%s",%d,"%s","%s","%s","%s","%d");'''
	for game in game_json:
		for answer in game['answers']:
			#print getDiseaseId(answer)     ## for testing only
			query = temp%(id,game['clue_id'],game['clue_name'],0,game['clue'],answer,game['answers'][answer],genRandomSet(835,getDiseaseId(answer)),getDiseaseId(answer))
			cursor.execute(query)
			id = id + 1
	db.commit()

def loadDiseaseData():
	id = 0
	temp = ''' INSERT INTO Diseases VALUES(%d,"%s"); '''
	for disease in data.diseases:
			query = temp%(id,disease)
			cursor.execute(query)
			id = id + 1
	db.commit()

if __name__ == '__main__':
	loadGeneData()
#	loadDiseaseData()
	db.close()
	print genRandomSet(50)		
