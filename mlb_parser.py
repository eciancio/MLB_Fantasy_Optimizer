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
		stats = mlbgame.player_stats(game.game_id)
		get_stats(1,stats,data)
                get_stats(0,stats,data)
	except:
		print('')
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
		print('')


def get_train_stats(team,stats,data,team_name):
	place = ""
	if team == 1:
		place = 'home_batting'
		s_p = stats['away_pitching'][0]
        else:
		place = 'away_batting'
		s_p = stats['home_pitching'][0]

	for player in stats[place]:
		compile_train_stats(player,s_p,data,team_name)


def get_stats(team,stats,data):
	place = ""
	if team == 1:
		place = 'home_batting'
		s_p = stats['away_pitching'][0]
        else:
		place = 'away_batting'
		s_p = stats['home_pitching'][0]

	for player in stats[place]:
		compile_stats(player,s_p,data)

def compile_train_stats(hitter,pitcher,data,team):
    if hitter.pos == 'P':
        pass
    else:
        stats = [hitter.name,
                hitter.pos, 
		hitter.avg,
		pitcher.era,
		hitter.h,
		team,
		hitter.obp,
		hitter.slg]
	data.append(stats)


def compile_stats(hitter,pitcher,data):
    if hitter.pos == 'P':
        pass
    else:
        stats = [hitter.name,
                hitter.pos, 
		hitter.avg,
		pitcher.era,
		hitter.h,
		hitter.obp,
		hitter.slg]
	data.append(stats)

def main():
    data = []
    get_batters(get_batch(2017,5),data)
    get_batters(get_batch(2016,8),data)
    get_batters(get_batch(2016,7),data)
    return data
