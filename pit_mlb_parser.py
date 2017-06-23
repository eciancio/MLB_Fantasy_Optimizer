from __future__ import print_function
import mlbgame

def get_batch(year,month):
	games = mlbgame.games(year, month)
	return games

def get_batters(games,data):
	for day in games:
		for game in day: 
			get_players(game,data)	
def get_players(game,data):
	try:
		home = ""
		away = ""
		home , away = get_team_names(game)	
                stats = mlbgame.player_stats(game.game_id)
		get_stats(1,stats,data,home)
                get_stats(0,stats,data,away)
	except:
		print('not_good')
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
	return team2, team1

def get_train_players(game,data):
	try:
		home = ""
		away = ""
		home , away = get_team_names(game)	
		stats = mlbgame.player_stats(game.game_id)
		get_train_stats(1,stats,data,home)
                get_train_stats(0,stats,data,away)
	except:
		print('not good')


def get_train_stats(team,stats,data,team_name):
	place = ""
	if team == 1:
		place = 'home_batting'
		s_p = stats['away_pitching'][0]
        else:
		place = 'away_batting'
		s_p = stats['home_pitching'][0]
        b_data = []
	for player in stats[place]:
		wL = compile_train_stats(player,s_p,b_data,team_name,team)
         
        pitcher = s_p 
        er = pitcher.er
        win = 0
        try:
            if pitcher.win:
                win = 1
        except:
            pass

        so = pitcher.so
        outs = pitcher.out
        # take avg of all  
        avg = 0.0
        r = 0.0
        obp = 0.0
        slg = 0.0
        bo = 0.0
        ops = 0.0
        for bat in b_data:
            avg += bat[2]
            r += bat[3]
            obp += bat[5]
            slg += bat[6]
            bo += bat[7]
            ops += bat[8]

        b_size = float(len(b_data)) + .00000001

        stats = [s_p.name,
                avg/b_size,
                r/b_size,
                obp/b_size,
                slg/b_size,
                bo/b_size,
                ops/b_size,
                wL,
                s_p.era,
                team_name]

        # append to data 
        data.append(stats)
                    

def compile_train_stats(hitter,pitcher,data,team,home):
    wL = .5
    try:
        wL=(float(pitcher.w)/float((pitcher.w+pitcher.l)))
    except:
        pass

    if hitter.pos == 'P':
        pass
    else:
        stats = [pitcher.name,
                hitter.pos, 
		hitter.avg,
		hitter.r,
		team,
		hitter.obp,
		hitter.slg,
                hitter.bo,
                hitter.ops,
                home]
	data.append(stats)
    return wL

def get_stats(team,stats,data,team_name):
	place = ""
	if team == 1:
		place = 'home_batting'
		s_p = stats['away_pitching'][0]
        else:
		place = 'away_batting'
		s_p = stats['home_pitching'][0]
        b_data = []
	for player in stats[place]:
		wL = compile_train_stats(player,s_p,b_data,team_name,team)
         
        pitcher = s_p 
        er = pitcher.er
        win = 0
        try:
            if pitcher.win:
                win = 1
        except:
            pass

        so = pitcher.so
        outs = pitcher.out

        points = (win * 6) + (er * -3) + (so * 3) + (outs)
        # take avg of all  
        avg = 0.0
        r = 0.0
        obp = 0.0
        slg = 0.0
        bo = 0.0
        ops = 0.0
        team = " "
        for bat in b_data:
            avg += bat[2]
            r += bat[3]
            slg += bat[6]
            obp += bat[5]
            bo += bat[7]
            ops += bat[8]

        b_size = float(len(b_data))
        stats = [s_p.name,
                avg/b_size,
                r/b_size,
                obp/b_size,
                slg/b_size,
                bo/b_size,
                ops/b_size,
                wL,
                s_p.era,
                team_name,
                points,
                s_p.s_so/float(s_p.s_ip+.0001)]
        # append to data 
        data.append(stats)
                    

def compile_stats(hitter,pitcher,data,team,home):
    wL = .5
    try:
        wL=(float(pitcher.w)/float((pitcher.w+pitcher.l)))
    except:
        pass

    if hitter.pos == 'P':
        pass
    else:
        stats = [hitter.name,
                hitter.pos, 
		hitter.avg,
		hitter.r,
		team,
		hitter.obp,
		hitter.slg,
                hitter.bo,
                hitter.ops,
                home]
	data.append(stats)
    return wL


def main():
    data = []
    get_batters(get_batch(2017,5),data)
    #get_batters(get_batch(2016,8),data)
    #get_batters(get_batch(2016,7),data)
    return data
