import requests
from bs4 import BeautifulSoup

def get_games():
    url = 'https://stream.lc/b/'


    sports = ['football', 'basketball', 'american-football', 'ice-hockey', 'billiard', 'darts', 'futsal', 'golf', 'handball', 'rugby-union', 'table-tennis', 'volleyball']
    selected_leagues = [
            ['CHAMPIONS LEAGUE', 'LA LIGA', 'LIGUE 1', 'CALCIO A', 'BUNDESLIGA'], 
            ['NBA'], 
            ['USA NFL'],
            ['NHL']]

    final_games = []

    for i in range(len(sports)):
        sporturl = url + sports[i] + '/'
        response = requests.get(sporturl)

        if response.status_code == 200:
            html_content = response.content

        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all table rows containing class 'pnltbl'
        table_rows = soup.find_all('tr', {'class': 'pnltbl table-light'})

        # Iterate through each table row and extract league, game, and link
        for row in table_rows:
            league_name = row.find_previous('tr', {'class': 'table-primary'})
            if league_name:
                league = league_name.text.strip()
                # Check if the row contains 'pnltblttl' class
                game_element = row.find('td', {'class': 'pnltblttl'})
                if game_element:
                    game = game_element.text.strip()
                    match_time = row.find('td', {'class': 'matchtime'}).text.strip()
                    link_element = game_element.find('a')
                    link = link_element['href'] if link_element else 'Link not found'

                    
                    teams = game.split('Vs')
                    if len(teams) > 1:
                        team1 = teams[0].strip()
                        team2 = teams[1].strip()
                    else:
                        team1 = game.strip()
                        team2 = ''

                    final_games.append([sports[i], league, team1, team2, match_time, link])

    return final_games

get_games()