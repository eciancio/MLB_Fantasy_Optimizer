# A simple script to scrape a web site and get some info about todays MLB games

#import the modules we are going to need
import requests
from bs4 import BeautifulSoup

def main():
# We will start by scraping the daily matchups from http://www.baseballpress.com/lineups
# First we set our website url
	url = "http://www.baseballpress.com/lineups/2017-06-23"

# Read the source code of our webpage and create a BeautifulSoup Object so we can 
# parse it and pull the data we want
	r = requests.get(url)
	data = r.text
	soup = BeautifulSoup(data)

# Each individual game appears to be contained within a class called "game clearfix" 
# so lets load that info in.
	games = soup.find_all("div", class_="team-data")
# Each game has two Teams that are playing and those team names are contained within a 
# class called "team-name".
# We will store these matchups in a dictionary, using the "matchup" as our dictionary key.
# Note that the first team in each game is the Visitor and the second is the home team

# Initialize our dictionary
	pitchers = []
# Loop through each game and pull out the team names.
	for element in games:
    		name = element.find_all(class_="player-link")
    		team = element.find_all(class_="team-name")
    		pair = []

    		for elemetn in team:
			pair.append(elemetn.get_text())
    		for dog in name:
			pair.append(dog.get_text())

    		pitchers.append(pair)


	return pitchers
# We now have a BS4 Result set that contains 2 items.  All we want is the text of each result.
# Remember the first result is the visiting team and the second is the home team.
# Lets grab these and make a nice descriptive key for our "matchups" dictionary
    
    # Now lets add the names of the home and visiting teams to our dictionary
#matchups


# Now that we have our daily matchups lets create a dictionary of the individual teams
# Each team has a link to it's daily lineup so lets store each teams unique url 
# so we can grab the lineups
# This is all still on the same page so we can use our original BS4 Object

# The individual team data appears to be in a class called "team-data".

# Once again lets loop through each team and get the "Name" and the link to it's lineup,
# Storing them in a "team" dictionary.

    
    # the url to the teams lineup is seen in the line "<a href="/team-lineups/TEAM">"
    # So lets grab that and set the url in our Teams dictionary
#teams


# Get the names of the players and make a players dictionary by going to the indiviual 
# teams websites and grabbing the names of their starting lineups.
#    playerdata = soup.find_all("div",class_="team-data")
    # The names are all in class "player-link" so we will loop through them and grab the names
 #   playerlist = playerdata.find_all(class_="player-link")
        
#players
