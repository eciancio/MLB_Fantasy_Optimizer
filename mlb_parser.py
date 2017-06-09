from __future__ import print_function
import mlbgame

def get_batch(year,month):
	games = mlbgame.games(year, month)
	return games

def get_batters(games):
	for day in games:
		for game in day: 
			get_players(game.game_id)	
def get_players(game_id):
	try:
		stats = mlbgame.player_stats(game_id)
		get_stats(1,stats)
	except:
		print('')

def get_stats(team,stats):
	place = ""
	if team == 1:
		place = 'home_batting'
		s_p = stats['away_pitching'][0]
	
	for player in stats[place]:
		compile_stats(player,s_p)

def compile_stats(hitter,pitcher):
	stats = [hitter.pos, 
		hitter.avg,
		pitcher.era,
		hitter.h]
	player = { hitter.name : stats}	
	data.append(player)

data = []
get_batters(get_batch(2017,5))

for i in range(100):
	print(data[i])
