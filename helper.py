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

inv_abr = {v: k for k, v in team_abr.iteritems()}

f_name = sys.argv[1]
names = {}
with open(f_name, 'rb') as csvfile:
    reader = csv.reader(csvfile,delimiter=' ')
    for line in reader:
        first_name=(line[0].split(','))
        last_name=(line[1].split(','))
        try:
# first_name[2][1:len(first_name[2])-1] + " " + l
            name = last_name[0][0:len(last_name[0])-1]
            sal = last_name[4][1:len(last_name[4])-1]
            name = name + str(inv_abr[line[1].split(',')[6][1:4]])
            names[name] = sal        
        except:
            pass
print names

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
            name = n_line[2:len(n_line)-1] + team[2:len(team)-2]
            value[name] = [pred, team[2:len(team)-2], pos, n_line[2:len(n_line)-1]]
        else:
            n_line = line.split(',')[0]
            pred =  line.split(',')[2]
            team = line.split(',')[4]
            pos = line.split(',')[3]
            name = n_line[2:len(n_line)] + team[2:len(team)-2]
            value[name] = [pred, team[2:len(team)-2], pos, n_line[2:len(n_line)]]
print value

ratio = []
for name in value:
    try:
        val = float(value[name][0])
        price = float(names[name])
        ratio.append([value[name][3],1000 * val/price,value[name][1],value[name][2],value[name][0],price])
    except:
        print name

sorted_stats = sorted(ratio, key=itemgetter(1))
for i in sorted_stats:
    print(i)
