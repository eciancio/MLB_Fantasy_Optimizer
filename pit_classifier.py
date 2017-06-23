import pit_mlb_parser
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

tf.logging.set_verbosity(tf.logging.INFO)

#global variables 
x_pred = []
x_pred2 =[]
x_pred3 = []
x_pred4 = []
x_pred5 = []
x_pred6 = []
x_pred7 = []
x_pred8 = []
x_pred9 = []
train_name = []
team_name = []

data = []

#read in av data
x_train = []
x_train2 =[]
x_train3 = []
x_train4 = []
x_train5 = []
x_train6 = []
x_train7 = []
x_train8 = []
x_train9 = []   

x_test = []
x_test2 = []
x_test3 = []
x_test4 = []
x_test5 = []
x_test6 = []
x_test7 = []
x_test8 = []
x_test9 = []

#score data 
y_train = []
y_test = []

def get_training_data():
    data = pit_mlb_parser.main()
    testing_data = data[:600]
    train_data = data[600:]
    
    #format training data
    for data in train_data:
	x_train.append(data[1])
	x_train2.append(data[2])
        x_train3.append(data[3])
        x_train4.append(data[4])
	x_train5.append(data[5])
        x_train6.append(data[6])
        x_train7.append(data[7])
        x_train8.append(data[8]) 
        x_train9.append(float(data[11]))
    #format data for evaluation
    for data in testing_data:
	x_test.append(data[1])
        x_test2.append(data[2])
        x_test3.append(data[3])
        x_test4.append(data[4])
	x_test5.append(data[5])
        x_test6.append(data[6])
        x_test7.append(data[7])
        x_test8.append(data[8])
        x_test9.append(float(data[11]))
        
        
    #read in score data 
    for data in train_data:
        y_train.append(float(data[10]))
    
    for data in testing_data:
        y_test.append(float(data[10]))



def get_data(name,attempt):
        letter = str.lower(name.split()[1][0])
        last = str.lower(name.split()[1][:5])
        first = str.lower(name[:2])
        url = "players/" + letter + '/' + last + first + '0' + str(attempt) + '.shtml'
        return scraper.parse_tables(url)


def get_era(data):
    era = data['pitching_standard'][len(data['pitching_standard'])-1]['W-L%']
    return era

def get_spi(data):
    era = data['pitching_standard'][len(data['pitching_standard'])-1]
    spi = float(era['IBB'])/float(era['SV']) 
    return spi

def get_WL(data):
    wL = data['pitching_standard'][len(data['pitching_standard'])-1]['L']
    return wL



def get_todays_stats():

    teams_logged = []
    pre_data = []
    for game in yesterday:
        one, two = get_team_names(game)
        teams_logged.append(one)
        teams_logged.append(two)
        pit_mlb_parser.get_train_players(game,pre_data) 
    
    for game in two_days:
        one, two = get_team_names(game)
        if one not in teams_logged:
            teams_logged.append(one)
            stats = mlbgame.player_stats(game.game_id)
            pit_mlb_parser.get_stats(0,stats,pre_data,one)
        if two not in teams_logged:
            stats = mlbgame.player_stats(game.game_id)
            pit_mlb_parser.get_stats(1,stats,pre_data,two)

    pitchers = getlineups.main()
    for pitcher in pitchers:
    	try:
		pitcher.append(get_era(get_data(str(pitcher[1]),1)))
                pitcher.append(get_WL(get_data(str(pitcher[1]),1)))
                pitcher.append(get_spi(get_data(str(pitcher[1]),1)))
                pitcher.append(str(pitcher[1]))
	except:
		try:
			pitcher.append(get_era(get_data(str(pitcher[1]),2)))
                        pitcher.append(get_WL(get_data(str(pitcher[1]),2)))
                        pitcher.append(get_spi(get_data(str(pitcher[1]),2)))
                        pitcher.append(str(pitcher[1]))
		except:
			pitcher.append(5.00)
                        pitcher.append(.50)
                        pitcher.append(.25)
                        pitcher.append(str(pitcher[1]))
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
 	    matchups[team1] = (team2, 0)
	    matchups[team2] = (team1, 1)

    opp_era = dict(matchups)
    matchups2 = dict(matchups)

    for pitcher in pitchers:
        print pitcher
	if pitcher[0] == "Diamondbacks":
		pitcher[0] = "D-backs"
	matchups[pitcher[0]] = (pitcher[2], pitcher[3],pitcher[4],pitcher[5])


    print(matchups)	
    print("SIZE: " + str(len(pre_data)))
    for data in pre_data:
        try:    
            x_pred.append(data[1])
            x_pred2.append(data[2])
            x_pred3.append(data[3])
            x_pred4.append(data[4])
	    x_pred5.append(data[5])
	    x_pred6.append(data[6])
            print "Team name = " + str(data[9])
            x_pred7.append(float(matchups[data[9]][1]))
	    x_pred8.append(float(matchups[data[9]][0]))
	    x_pred9.append(float(matchups[data[9]][2]))
            train_name.append(matchups[data[9]][3])
            team_name.append(data[9])
        except:
            pass

    print train_name
    print("SIZE: " + str(len(pre_data)))

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

#set the scraper for baseball reference 
scraper = brscraper.BRScraper()

#read in data from the last 3 days
day = input("Day ")
month = input("Month ")
yesterday = mlbgame.day(2017, month, day - 1)
two_days = mlbgame.day(2017, month, day - 2)
today = mlbgame.day(2017, month, day)

#get todays stats for predict
get_todays_stats()

#get training stats to train
get_training_data()


#make columns 
COLUMNS= ['avg','era','hits']
test_continious_cols = []
test_labels = []

#avg column 
avg = tf.contrib.layers.real_valued_column("avg")
spi = tf.contrib.layers.real_valued_column("spi")
obp = tf.contrib.layers.real_valued_column("obp")
slg =  tf.contrib.layers.real_valued_column("slg")
bo =  tf.contrib.layers.real_valued_column("bo")
ops  =  tf.contrib.layers.real_valued_column("ops")
wL  =  tf.contrib.layers.real_valued_column("wL")
era  =  tf.contrib.layers.real_valued_column("era")

model_dir = 'pit_mlb_file'
opt = tf.train.GradientDescentOptimizer(learning_rate=0.01)
m = tf.contrib.learn.LinearRegressor(feature_columns=[slg,avg,era,wL,obp,ops,spi],
          model_dir=model_dir,optimizer=opt)
#,runs,obp,slg,bo,ops,
def input_fn_traint():
    #make cols
    continuous_cols = {'avg': tf.constant(x_train)}
    continuous_cols['spi'] = tf.constant((x_train9))
    continuous_cols['obp'] = tf.constant((x_train3))
    continuous_cols['slg'] = tf.constant((x_train4))
    continuous_cols['bo'] = tf.constant((x_train5))
    continuous_cols['ops'] = tf.constant((x_train6))
    continuous_cols['wL'] = tf.constant((x_train7))
    continuous_cols['era'] = tf.constant((x_train8))

    labels = tf.constant(y_train)
    return continuous_cols, labels

def input_fn_test():
    test_continuous_cols = {'avg': tf.constant(x_test)}
    test_continuous_cols['spi'] = tf.constant(x_test9)
    test_continuous_cols['obp'] = tf.constant(x_test3)
    test_continuous_cols['slg'] = tf.constant(x_test4)
    test_continuous_cols['bo'] = tf.constant(x_test5)
    test_continuous_cols['ops'] = tf.constant(x_test6)
    test_continuous_cols['wL'] = tf.constant(x_test7)
    test_continuous_cols['era'] = tf.constant(x_test8)

    test_labels = tf.constant(y_test)
    return test_continuous_cols, test_labels



def input_fn_pred():
    test_continuous_cols = {}
    test_continuous_cols = {'avg': tf.constant(x_pred)}
    test_continuous_cols['spi'] = tf.constant(x_pred9)
    test_continuous_cols['obp'] = tf.constant(x_pred3)
    test_continuous_cols['slg'] = tf.constant(x_pred4)
    test_continuous_cols['bo'] = tf.constant(x_pred5)
    test_continuous_cols['ops'] = tf.constant(x_pred6)
    test_continuous_cols['wL'] = tf.constant(x_pred7)
    test_continuous_cols['era'] = tf.constant(x_pred8)

    return test_continuous_cols



m.fit(input_fn=input_fn_traint, steps=1000)
results = m.evaluate(input_fn=input_fn_test, steps=1)
for key in sorted(results):
    print("%s: %s" % (key, results[key]))


predict_class = m.predict(input_fn=input_fn_pred)
i = 0
pre = list(predict_class)
inner = []
full = []
with open("prediction/all.txt",'a') as preds:
    for pred in pre:
        inner = [train_name[i].split()[1],pred,'P',team_name[i]]
        print inner
        full.append(inner)
    #    preds.write(str(inner))
     #   preds.write('\n')
        i+= 1    

'''
final_array =[]

for i in range(len(all_class)):
    inner_array = [train_name[i],all_class[i],x_pred3[i],team_name[i]]
    final_array.append(inner_array)

sorted_final = sorted(final_array, key=itemgetter(1))
for i in range(20):
    print(sorted_final[len(sorted_final)-1 - i])

more_data = {}
for i in sorted_final:
    if more_data.get(i[3]) == None:
        array = [i[1]]
        more_data[i[3]] = array
    else:
        more_data[i[3]].append(i[1])

best_pitchers = []
for dat in more_data:
    inner_array = []
    inner_array.append(dat)
    inner_array.append(sum(more_data[dat])/float(len(more_data[dat])))
    best_pitchers.append(inner_array)

sorted_pitchers = sorted(best_pitchers, key=itemgetter(1))

with open('prediction/pitchers.txt','w') as stream:
    for team in sorted_pitchers:
        stream.write(str(team))

def print_to_txt(data,pos):
	name = 'prediction/' + pos + ".txt"
	with open(name, 'w') as stream:
		if pos == 'OF':
			for dat in data:
				if dat[2] == 'LF' or dat[2] == 'RF' or dat[2] == 'CF':
					stream.write(str(dat))
					stream.write('\n')
		elif pos == '2B':
			 for dat in data:
                                if dat[2] == '2B' or dat[2] == '3B-2B':
                                        stream.write(str(dat))
                                        stream.write('\n')
		else:
			 for dat in data:
                                if dat[2] == pos:
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
    return feature_cols, label'''
