from __future__ import print_function
import mlbgame

def get_batch(year,month):
	games = mlbgame.games(year, month)
	return games

def get_batters(games,data):
	for day in games:
		for game in day: 
			get_players(game.game_id,data)	
def get_players(game_id,data):
	try:
		stats = mlbgame.player_stats(game_id)
		get_stats(1,stats,data)
                get_stats(0,stats,data)
	except:
		print('')

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

def compile_stats(hitter,pitcher,data):
    if hitter.pos == 'P':
        pass
    else:
        stats = [hitter.name,
                hitter.pos, 
		hitter.avg,
		pitcher.era,
		hitter.h]
	data.append(stats)

def main():
    data = []
    get_batters(get_batch(2017,5),data)
    get_batters(get_batch(2016,8),data)
    get_batters(get_batch(2016,7),data)
    return data
