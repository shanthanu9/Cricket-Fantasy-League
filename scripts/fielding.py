import requests
from bs4 import BeautifulSoup
import pandas as pd

PAGES = 52

players = []

for page in range(1, PAGES+1):
    URL = "http://stats.espncricinfo.com/ci/engine/stats/index.html?class=2;template=results;type=fielding;page="+str(page)
    r = requests.get(URL)

    soup = BeautifulSoup(r.content, 'html5lib')

    # print(soup.prettify())

    tables = soup.find_all('table')

    table = None
    for t in tables:
        if t.caption != None and t.caption.text == 'Overall figures':
            table = t
            break

    if table == 'None':
        print('Error: Cricinfo has probably updated their website! So this scraping script is no longer valid:(')
        exit()

    header = []

    for heading in table.thead.tr.findAll('a'):
        header.append(heading.text)

    for row in table.tbody.findAll('tr'):
        player = {}
        i = 0
        for data in row.findAll('td'):
            if data.text is not "":
                player[header[i]] = data.text
                i += 1
        players.append(player)
    
    print("Page "+str(page)+" done!")

# Create a dataframe from players list
df = pd.DataFrame(players)

# Save to csv
df.to_csv('fielding.csv')