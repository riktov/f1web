"""Module for scraping information from Wikipedia"""

import re
import urllib.request
from bs4 import BeautifulSoup
from bs4 import element
from pprint import pp

WIKIPEDIA_BASE_URL = "https://en.wikipedia.org/wiki/"

def parse_team_or_driver(tr):
    return [ s for s in tr.strings if s != ' ' and s != '\n']
    return tr.string

def is_entrant_or_driver(td):
    return type(td) is element.Tag and td.find_all("span", attrs={"class": "flagicon"})

def parse_head_row(tr):
    return parse_team_or_driver(tr[1])

def parse_driver(td):
    country = td.find("span", attrs={"class":"flagicon"})
    driver = country.next_sibling.next_sibling

    return {
        "name":driver.get_text(' ', strip=True),
        "country": country.find('a')['title'],
    }
    return td.get_text(' ', strip=True)

def blank_entry():
    return {
        "drivers": [],
        "cars": []
    }

def element_joined_strings(elem):
    return ' '.join([s for s in elem.stripped_strings])

def scrape_season(article_name):
    url = WIKIPEDIA_BASE_URL + article_name

    f = urllib.request.urlopen(url)   
    soup = BeautifulSoup(f, "html.parser")

    sect_hed_dc = soup.find('h2', id='Drivers_and_constructors')
    sect_hed_td = soup.find('h2', id='Teams_and_drivers')

    sect_hed = sect_hed_dc or sect_hed_td
    # if not sect_hed:
    #     sect_hed = sect_hed_td

    mw_heading = sect_hed.parent
    # 1982 wraps the table within a table without the wikitable class
    table = mw_heading.findNextSibling("table")
    # table = mw_heading.findNextSibling(attrs={"class":"wikitable"})
    tbody = table.find('tbody')

    headings = table.find("thead")
    entries = []

    this_entry = blank_entry()
    prev_number = 0

    for tr in tbody.children:
        if type(tr) is element.Tag:
            if tr.parent is headings:
                print("This is the header, which we should skip.")

            span_flags = tr.find_all("span", attrs={"class": "flagicon"})

            tds = [ td for td in tr.children if td != '\n' ] 
            # print(tds)

            if len(span_flags) == 0:
                # print("This is a row without a flag.")
                continue  

            if len(span_flags) > 1:
                # save the current, create new one
                if "constructor" in this_entry:
                    entries.append(this_entry)
                    this_entry = blank_entry()

                # tds = span_flags[0].parent.parent

                td_entrant = tds[0]
                entrant = td_entrant.get_text(' ', strip=True)

                # print("\nEntrant:", entrant)
                this_entry["entrant"] = entrant
                
                td_constructor = tds[1]
                #We want only the chassis constructor; "McLaren", not "McLaren-Honda"
                constructor = td_constructor.contents[0].string
                # print("Constructor:", constructor)
                this_entry["constructor"] = constructor

                td_cars = tds[2]
                cars = [ elem.string for elem in td_cars]
                # print(cars)
                cars = [ str(c).strip() for c in cars if c != '\n' and c is not None]
                
                this_entry["cars"] = cars
                # print("Cars:", cars)

            td_rounds = tds[-1]
            rounds = td_rounds.get_text(' ', strip=True)
            
            td_driver = tds[-2]
            driver = parse_driver(td_driver)

            number = None

            # if multiple drivers share a number, it is only on the first of the lines
            if len(tds) > 2: #number, name, rounds
                td_number = tds[-3]
                num_text = td_number.get_text(' ', strip=True)
                num_text = re.sub(r"\D", "", num_text) 
                number = int(num_text)
            else: #only name and rounds, so use the same number
                number = prev_number
            
            # print("Driver:", driver)

            driver_info = {
                "driver": driver,
                "rounds": rounds,
                "number": number
            }
            this_entry["drivers"].append(driver_info)

            prev_number = number
    return entries

if __name__ == "__main__":
    specs = scrape_season("1989_Formula_One_World_Championship")
    pp(specs)
