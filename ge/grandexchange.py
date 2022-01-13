import pandas as pd
import urllib.request
from bs4 import BeautifulSoup

class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"

url = 'https://oldschool.runescape.wiki/w/Category:Grand_Exchange_items'
opener = AppURLopener()
item_dict = {"items":[],'buy_limit':[],'high_alch':[],'members':[],'vol':[]}
not_last_page = True
page = 0

while not_last_page == True:
    response = opener.open(url)
    soup = BeautifulSoup(response, features='lxml')
    item_list = soup.find(id = 'mw-content-text')
    for ultag in item_list.find_all('ul'):
        for litag in ultag.find_all('li'):
            item_url = 'https://oldschool.runescape.wiki' + litag.find('a')['href']
            item_response = opener.open(item_url)
            item_soup = BeautifulSoup(item_response, features='lxml')
            html = str(item_soup)
            tables = pd.read_html(html, index_col = 1)
            for table in tables:
                if 'Released' in str(table):
                  table = table.iloc[:,[-1]]
                  print(table)
                  item_dict['items'].append(litag.text)
                  item_dict['buy_limit'].append(table.loc['Buy limit'])
                  item_dict['high_alch'].append(table.loc['High alch'])
                  item_dict['members'].append(table.loc['Members'])
                  item_dict['vol'].append(table.loc['Daily volume'])
                  break
                else:
                    break
    ge_items = pd.DataFrame(item_dict)

    ge_items.to_csv('ge_data\ge_items.csv')                           

    url_checker = soup.find_all('a',{'title' : 'Category:Grand Exchange items'})

    if len(url_checker) == 2:
        url = 'https://oldschool.runescape.wiki' + url_checker[0]['href']
    else:
        url = 'https://oldschool.runescape.wiki' + url_checker[1]['href']
    
    print(url)

    if url == None:
        not_last_page = False    