"""Module for scraping information from Wikipedia"""

import urllib.request
from bs4 import BeautifulSoup
from bs4 import element

WIKIPEDIA_BASE_URL = "https://en.wikipedia.org/wiki/"

def parse_engine_count(s):
    s = s.strip()
    parts = s.split('×')
    return int(parts[0].strip())

def parse_engine_name(s):
    parts = s.split(' ')
    
    #if the first part has a hyphen, then that is a British maker name
    if '-' in parts[0]:
        maker = parts[0]
        designation = ' '.join(parts[1:])
        return (maker, designation)
    else:   
        designation = parts[-1]
        maker = ' '.join(parts[0:-1]) 
        return (maker, designation)

def scrape_season_cars(article_name):
    url = WIKIPEDIA_BASE_URL + article_name

    f = urllib.request.urlopen(url)   
    soup = BeautifulSoup(f, "html.parser")

    sect_hed_dc = soup.find('h2', id='Drivers_and_constructors')
    sect_hed_td = soup.find('h2', id='Teams_and_drivers')

    sect_hed = sect_hed_dc
    if not sect_hed:
        sect_hed = sect_hed_td

    mw_heading = sect_hed.parent
    table = mw_heading.findNextSibling(attrs={"class":"wikitable"})
    tbody = table.find('tbody')

    for tr in tbody.children:
        if type(tr) is element.Tag:
            tds = tr.children
            #if there are more than three tds, it is the first row
            # if len(tds) > 3:
            # print("!!------!!")
            idx = 0 
            for td in tds:
                # print(f"%%---{idx}---%%")
                if idx == 5:
                    a_tags = td.find_all('a')
                    for tag in a_tags:
                        print(tag['title'])
                idx += 1

    return {
        "engine_count": 1,
        "engine_name": 2
    }

if __name__ == "__main__":
    specs = scrape_season_cars("1989_Formula_One_World_Championship")
    print(specs)