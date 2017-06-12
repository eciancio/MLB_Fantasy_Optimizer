import mlb_parser
import tensorflow as tf
import os 
import urllib
import numpy as np
import tempfile
import urllib
import mlbgame
from operator import itemgetter
import brscraper
import getlineups
scraper = brscraper.BRScraper()

day = input("Day ")
month = input("Month ")
yesterday = mlbgame.day(2017, month, day - 1)
two_days = mlbgame.day(2017, month, day - 2)
today = mlbgame.day(2017, month, day)

def get_team_names(game):
        if len(str(game).split()) == 5:
		team1 = str(game).split()[0]
		team2 = str(game).split()[3]
	else: 
		if str(game).split()[2] == 'at':
			team1 = str(game).split()[0]
			team2 = str(game).split()[3] + ' ' + str(game).split()[4]
		else:
			team1 = str(game).split()[0] + ' '+ str(game).split()[1]
			team2 = str(game).split()[4]
        
        return team1, team2

teams_logged = []
pre_data = []
for game in yesterday:
    one, two = get_team_names(game)
    teams_logged.append(one)
    teams_logged.append(two)
    mlb_parser.get_train_players(game,pre_data) 
print(teams_logged)
for game in two_days:
    one, two = get_team_names(game)
    if one not in teams_logged:
        print(one)
        mlb_parser.get_train_players(game,pre_data)
    if two not in teams_logged:
        print(two)
        mlb_parser.get_train_players(game,pre_data)

def get_data(name,attempt):
	letter = str.lower(name.split()[1][0])
	last = str.lower(name.split()[1][:5])
	first = str.lower(name[:2])
	url = "players/" + letter + '/' + last + first + '0' + str(attempt) + '.shtml'
	return scraper.parse_tables(url)

def get_era(data):
	
	era = data['pitching_standard'][len(data['pitching_standard'])-1]['W-L%']
	return era

pitchers = getlineups.main()
for pitcher in pitchers:
	try:
		pitcher.append(get_era(get_data(str(pitcher[1]),1)))
	except:
		try:
			pitcher.append(get_era(get_data(str(pitcher[1]),2)))
		except:
			pitcher.append(5.00)



opp_era = {}


matchups= {}
for game in today:
        score1 = '(0)'
        score2 = '(0)'
	if len(str(game).split()) == 5:
		team1 = str(game).split()[0]
		team2 = str(game).split()[3]
                score1, score2 = str(game).split()[1], str(game).split()[4]
	else: 
		if str(game).split()[2] == 'at':
			team1 = str(game).split()[0]
			team2 = str(game).split()[3] + ' ' + str(game).split()[4]
                        score1, score2 = str(game).split()[1],str(game).split()[5]
		else:
			team1 = str(game).split()[0] + ' '+ str(game).split()[1]
			team2 = str(game).split()[4]
                        score1, score2 = str(game).split()[2],str(game).split()[5]
        
        if score1 == '(0)' and score2 == '(0)':
 	    matchups[team1] = team2
	    matchups[team2] = team1

print(matchups)
opp_era = dict(matchups)
matchups2 = dict(matchups)
for pitcher in pitchers:
	if pitcher[0] == "Diamondbacks":
		pitcher[0] = "D-backs"
	matchups[pitcher[0]] = pitcher[2]

new_opp = {}
for i in opp_era:
	print(i)
	print(matchups2[i])
	new_opp[i] = matchups[matchups2[i]]

print(new_opp)	


x_pred = []
x_pred2 =[]
x_pred3 = []
x_pred4 = []
x_pred5 = []
train_name = []
team_name = []
print("SIZE: " + str(len(pre_data)))
for data in pre_data:
        try:
            x_pred2.append(float(new_opp[data[5]]))
	    x_pred.append(data[2])
	    x_pred3.append(data[1])
	    x_pred4.append(data[6])
	    x_pred5.append(data[7])
            train_name.append(data[0])
            team_name.append(data[5])
        except:
            pre_data.remove(data) 
print("SIZE: " + str(len(pre_data)))

train_file = tempfile.NamedTemporaryFile()
test_file = tempfile.NamedTemporaryFile()

data = mlb_parser.main()

testing_data = data[:300]
train_data = data[300:]
print len(train_data)

#read in av data
x_train = []
x_train2 =[]
x_train3 = []
x_train4 = []
x_train5 = []
for data in train_data:
	x_train.append(data[2])
	x_train2.append(data[3])
        x_train3.append(data[1])
        x_train4.append(data[5])
	x_train5.append(data[6])
x_test = []
x_test2 = []
x_test3 = []
x_test4 = []
x_test5 = []
for data in testing_data:
	x_test.append(data[2])
        x_test2.append(data[3])
        x_test3.append(data[1])
        x_test4.append(data[5])
	x_test5.append(data[6])
#read in hit data 
y_train = []
for data in train_data:
    if data[4] > 0:
    	data[4] = 1
    y_train.append(int(data[4]))
y_test = []
for data in testing_data:
    if data[4] > 0:
        data[4] = 1
    y_test.append(int(data[4]))


#make columns 
COLUMNS= ['avg','era','hits']
test_continious_cols = []
test_labels = []

#avg column 
avg = tf.contrib.layers.real_valued_column("avg")
era = tf.contrib.layers.real_valued_column("era")
pos = tf.contrib.layers.sparse_column_with_hash_bucket("pos", hash_bucket_size=1000)
obp =  tf.contrib.layers.real_valued_column("obp")
slg =  tf.contrib.layers.real_valued_column("slg")


model_dir = tempfile.mkdtemp()
m = tf.contrib.learn.LinearClassifier(feature_columns=[avg,era,pos,obp,slg],
          model_dir=model_dir)

def input_fn_traint():
    #make cols
    continuous_cols = {'avg': tf.constant(x_train)}
    continuous_cols['era'] = tf.constant((x_train2))
    continuous_cols['obp'] = tf.constant((x_train4))
    continuous_cols['slg'] = tf.constant((x_train5))
    continuous_cols['pos'] = tf.SparseTensor(
            indices=[[i, 0] for i in range(len(x_train3))],
            values=x_train3,
            dense_shape=[len(x_train3), 1])

    labels = tf.constant(y_train)
    return continuous_cols, labels

def input_fn_test():
    test_continuous_cols = {'avg': tf.constant(x_test)}
    test_continuous_cols['era'] = tf.constant(x_test2)
    test_continuous_cols['obp'] = tf.constant(x_test4)
    test_continuous_cols['slg'] = tf.constant(x_test5)
    test_continuous_cols['pos'] =tf.SparseTensor(
            indices=[[i, 0] for i in range(len(x_test3))],
            values=x_test3,
            dense_shape=[len(x_test3), 1])

    test_labels = tf.constant(y_test)
    return test_continuous_cols, test_labels



def input_fn_pred():
    test_continuous_cols = {'avg': tf.constant(x_pred)}
    test_continuous_cols['era'] = tf.constant(x_pred2)
    test_continuous_cols['obp'] = tf.constant(x_pred4)
    test_continuous_cols['slg'] = tf.constant(x_pred5)
    test_continuous_cols['pos'] =tf.SparseTensor(
            indices=[[i, 0] for i in range(len(x_pred3))],
            values=x_pred3,
            dense_shape=[len(x_pred3), 1])

    test_labels = tf.constant(y_test)
    return test_continuous_cols, test_labels





m.fit(input_fn=input_fn_traint, steps=10000)
results = m.evaluate(input_fn=input_fn_test, steps=1)
for key in sorted(results):
        print("%s: %s" % (key, results[key]))
predictions = m.predict_proba(input_fn=input_fn_pred)
predict_array =[]
for classs in predictions:
    predict_array.append(classs)

final_array =[]
for i in range(len(predict_array)):
    inner_array = [train_name[i],predict_array[i][0],predict_array[i][1],x_pred3[i],team_name[i]]
    final_array.append(inner_array)

sorted_final = sorted(final_array, key=itemgetter(1))
for i in range(20):
    print(sorted_final[i])

more_data = {}
for i in sorted_final:
    if more_data.get(i[4]) == None:
        array = [i[2]]
        more_data[i[4]] = array
    else:
        more_data[i[4]].append(i[2])

best_pitchers = []
for dat in more_data:
    inner_array = []
    inner_array.append(dat)
    inner_array.append(sum(more_data[dat])/float(len(more_data[dat])))
    best_pitchers.append(inner_array)

sorted_pitchers = sorted(best_pitchers, key=itemgetter(1))
print(sorted_pitchers)
def print_to_txt(data,pos):
	name = pos + ".txt"
	with open(name, 'w') as stream:
		if pos == 'OF':
			for dat in data:
				if dat[3] == 'LF' or dat[3] == 'RF' or dat[3] == 'CF':
					stream.write(str(dat))
					stream.write('\n')
		elif pos == '2B':
			 for dat in data:
                                if dat[3] == '2B' or dat[3] == '3B-2B':
                                        stream.write(str(dat))
                                        stream.write('\n')
		else:
			 for dat in data:
                                if dat[3] == pos:
                                        stream.write(str(dat))
                                        stream.write('\n')
positions = ['1B','2B','3B','SS','OF','C']

for position in positions:
	print_to_txt(sorted_final,position)

def input_fn(df):
    # Creates a dictionary mapping from each continuous feature column name (k) to
    # the values of that column stored in a constant Tensor.
    continuous_cols = {k: tf.constant(df[k].values)
            for k in CONTINUOUS_COLUMNS}
    # Creates a dictionary mapping from each categorical feature column name (k)
    # to the values of that column stored in a tf.SparseTensor.
    categorical_cols = {k: tf.SparseTensor(
        indices=[[i, 0] for i in range(df[k].size)],
        values=df[k].values,
        dense_shape=[df[k].size, 1])
        for k in CATEGORICAL_COLUMNS}
    # Merges the two dictionaries into one.
    feature_cols = dict(continuous_cols.items() + categorical_cols.items())
    # Converts the label column into a constant Tensor.
    label = tf.constant(df[LABEL_COLUMN].values)
    # Returns the feature columns and the label.
    return feature_cols, label







