import csv
from operator import itemgetter
import sys

team_abr = {}
team_abr["Orioles"] ="BAL" 
team_abr["Indians"] ="CLE" 
team_abr["Braves"] ="ATL" 
team_abr["Giants"] ="SFG" 
team_abr["Marlins"] ="MIA" 
team_abr["Cubs"] ="CHC" 
team_abr["Yankees"] ="NYY" 
team_abr["Angels"] ="LAA" 
team_abr["Dodgers"] ="LOS" 
team_abr["Twins"] ="MIN" 
team_abr["Mets"] ="NYM" 
team_abr["White Sox"] ="CWS" 
team_abr["Rockies"] ="COL" 
team_abr["D-backs"] ="ARI" 
team_abr["Phillies"] ="PHI" 
team_abr["Cardinals"] ="STL" 
team_abr["Athletics"] ="OAK" 
team_abr["Astros"] ="HOU" 
team_abr["Mariners"] ="SEA" 
team_abr["Tigers"] ="DET" 
team_abr["Brewers"] ="MIL" 
team_abr["Pirates"] ="PIT" 
team_abr["Rangers"] ="TEX" 
team_abr["Blue Jays"] ="TOR" 
team_abr["Red Sox"] ="BOS" 
team_abr["Royals"] ="KAN" 
team_abr["Reds"] ="CIN" 
team_abr["Rays"] ="TAM" 
team_abr["Nationals"] ="WAS" 
team_abr["Padres"] ="SDP" 


class Player(object):
    def __init__(self, name, val, wt):
        self.name = name
        self.val = val
        self.wt = wt

class Catcher(Player):
    limit = 1
class Pitcher(Player):
    limit = 1
class First(Player):
    limit = 1
class Second(Player):
    limit = 1
class Short(Player):
    limit = 1
class Third(Player):
    limit = 1
class OutField(Player):
    limit = 3



class MlbKnapsack(object):
    def __init__(self,budget):
        self.all_players = []
        self.budget = budget

    def add_player(self,player):
        self.all_players.append(player)

    def get_len(self):
        print len(self.all_players)

    def position_count(self, team, player):
        total = 0 
        for p in team:
            if type(p) == type(player):
                total += 1
        return total


knap = MlbKnapsack(320)


inv_abr = {v: k for k, v in team_abr.iteritems()}
named = []
f_name = sys.argv[1]
names = {}
ordered_names = []
with open(f_name, 'rb') as csvfile:
    reader = csv.reader(csvfile,delimiter=' ')
    for line in reader:
        first_name=(line[0].split(','))
        last_name=(line[1].split(','))
        try:
# first_name[2][1:len(first_name[2])-1] + " " + l
            name = last_name[0][0:len(last_name[0])-1]
            sal = last_name[4][1:len(last_name[4])-1]
            name = name + str(inv_abr[line[1].split(',')[6][1:4]]) + first_name[1][1:len(first_name[1])-1]
            names[name] = sal, first_name[1] 
            ordered_names.append(name)
        except:
            pass
print named

value = {}
with open("prediction/all.txt",'r') as text:
    srting= text.read()
    srting = srting.split('\n')
    srting = srting[:len(srting)-1]
    for line in srting:
        if len(line.split(',')) == 4:
            n_line = line.split(',')[0]
            pred = line.split(',')[1]
            team = line.split(',')[3]
            pos = line.split(',')[2]
            pos = pos[2:len(pos)-1]
            if pos == "LF" or pos == "RF" or pos == "CF":
                pos = "OF"

            name = n_line[2:len(n_line)-1] + team[2:len(team)-2] + pos
            value[name] = [pred, team[2:len(team)-2], pos, n_line[2:len(n_line)-1]]
        else:
            n_line = line.split(',')[0]
            pred =  line.split(',')[2]
            team = line.split(',')[4]
            pos = line.split(',')[3]
            name = n_line[2:len(n_line)] + team[2:len(team)-2]
            value[name] = [pred, team[2:len(team)-2], pos, n_line[2:len(n_line)]]
#print value

values = []
prices = []

ratio = []
for name in ordered_names:
    try:
        val = float(value[name][0])
        price = float(names[name][0])
        position = names[name][1]
        values.append(int(val*100))
        prices.append(int(price/100))
        named.append(name)
        if position == "\"C\"":
            knap.add_player(Catcher(name,val,price))
        elif position == "\"P\"":
            knap.add_player(Pitcher(name,val,price))
        elif position == "\"1B\"":
            knap.add_player(First(name,val,price))
        elif position == "\"2B\"":
            knap.add_player(Second(name,val,price))
        elif position == "\"3B\"":
            knap.add_player(Third(name,val,price))
        elif position == "\"SS\"":
            knap.add_player(Short(name,val,price))
        elif position == "\"OF\"":
            knap.add_player(OutField(name,val,price))

        ratio.append([value[name][3],1000 * val/price,value[name][1],value[name][2],value[name][0],price])
    except:
        pass

sorted_stats = sorted(ratio, key=itemgetter(1))
for i in sorted_stats:
    pass
    #print(i)

for i in range(5):
    print ordered_names[i]
print len(named)
named.append("Nothing")
print len(prices)
def knapSack(W, wt, val, n, named):
    K = [[0 for x in range(W+1)] for x in range(n+1)]  
    # Build table K[][] in bottom up manner
    for j in range(n+1):
        for i in range(W+1):
            K[j][i] = [0,""]
    for i in range(n+1):
        limit = 0
        for w in range(W+1):

            if i != 0:
                player = knap.all_players[i-1]
                limit = player.limit
                namled = list(K[i-1][w-wt[i-1]][1])
            if i==0 or w==0:
                K[i][w] = [0, []]
            elif wt[i-1] > w:
                K[i-1][w]
                continue
            elif limit <= knap.position_count(namled, player):
                K[i][w] = K[i-1][w]
                continue
            elif wt[i-1] <= w:
                if val[i-1] + K[i-1][w-wt[i-1]][0] > K[i-1][w][0]:
                    namles = list(K[i-1][w-wt[i-1]][1]) 
                    namles.append(player)
                    K[i][w] = val[i-1]+K[i-1][w-wt[i-1]][0] , namles
                else:
                    namles =  K[i-1][w][1]
                    K[i][w] = K[i-1][w][0], namles

            else: 
                K[i][w] = K[i-1][w]
                
    return K[n][W]

print "cat"
knap.get_len()
result = knapSack(350, prices, values, int(len(prices)),named)[1]
tot = 0
for i in result:
    print i.name, i.val, i.wt
    tot += i.val

print tot
