import os
import requests

from fake_useragent import UserAgent

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


class rank_scraper:

    def __init__(self,MODE,URL):

        # When set to 0, will provide name, avatar URL, current rank icon URL, best rank icon URL.
        # When set other than 0, will provide only current rank and best rank names in plain text using the RANK_INDEX.
        self.MODE = MODE

        # The Steam profile URL of the targeted player.
        self.PROFILE_URL = URL

        self.RANK_INDEX = {"1":"SILVER I",
                    "2":"SILVER II",
                    "3":"SILVER III",
                    "4":"SILVER IV",
                    "5":"SILVER ELITE",
                    "6":"SILVER ELITE MASTER",
                    "7":"GOLD NOVA I",
                    "8":"GOLD NOVA II",
                    "9":"GOLD NOVA III",
                    "10":"GOLD NOVA MASTER",
                    "11":"MASTER GUARDIAN I",
                    "12":"MASTER GUARDIAN II",
                    "13":"MASTER GUARDIAN ELITE",
                    "14":"DISTINGUISHED MASTER GUARDIAN",
                    "15":"LEGENDARY EAGLE",
                    "16":"LEGENDARY EAGLE MASTER",
                    "17":"SUPREME MASTER FIRST CLASS",
                    "18":"THE GLOBAL ELITE",}

        # Initializing the chromedriver:
        self.OPTIONS = Options()
        self.OPTIONS.add_argument('disable-blink-features=AutomationControlled')
        self.OPTIONS.add_argument(f'user-agent={UserAgent().random}')
        self.OPTIONS.headless = True

        self.DRIVER = webdriver.Chrome(self.config_driver(),options=self.OPTIONS)

    def config_driver(self):
        
        ''' Setup driver path. '''

        DRIVER_PATH = ''
        
        if os.path.isfile("driver_path.txt"):
            with open("driver_path.txt",'r') as f:
                DRIVER_PATH = f.read()

                if not os.path.isfile(DRIVER_PATH):
                    print("ERROR: Invalid Path to Driver in driver_path.txt. Re-run the script to enter path.")
                    
                    os.remove("driver_path.txt")
                    exit()
        else:
            while True:
                DRIVER_PATH = input("Enter the path to chromedriver: ")
            
                if os.path.isfile(DRIVER_PATH):
                    with open('driver_path.txt','w') as f:
                        f.write(DRIVER_PATH)
                    break
                else:
                    print("INCORRECT PATH: chromedriver NOT FOUND AT THE SPECIFIED LOCATION!")

        return DRIVER_PATH


    def get_imgs(self, ID):
        
        ''' Scrape avatar and rank images using the webdriver.'''

        AVATAR = ''
        RANKS = []

        self.DRIVER.get(f"https://csgostats.gg/player/{ID}")
        
        for src in self.DRIVER.find_elements(By.CSS_SELECTOR,'img'):

            if AVATAR and len(RANKS) == 2:
                break
            else:
                
                if 'avatars' in src.get_attribute('src'):

                    AVATAR = src.get_attribute('src')
                
                if 'ranks' in src.get_attribute('src'):
                    if self.MODE == 1:
                        RANKS.append(self.RANK_INDEX[src.get_attribute('src').split('/')[5][:-4]])
                    else:
                        RANKS.append(src.get_attribute('src'))

        self.DRIVER.close()

        if self.MODE == 1:
            AVATAR = None

        return AVATAR, RANKS

    def get_steamid_name(self, URL):
        
        '''
     Get steam profile name and steamID64 using just a GET request. Selenium not needed here.	
     csgostats.gg uses steamID64 to find players. That is why we have to get it from player's steam profile page.

        '''

        NAME, STEAM_ID = '',''

        r = requests.get(URL,headers = {'user-agent':UserAgent().random})

        for _ in r.content.decode().split('\n'):

            if NAME and STEAM_ID:
                break
            else:

                if "<title>" in _.lstrip():
                    NAME = _.split('::')[1].split('<')[0]

                elif '"owner"' in _:
                    
                    STEAM_ID = _.split(',')[4].split(':')[1].strip('"')

        return NAME, STEAM_ID


    # Call everything and get the job done
    def run(self):
        
        NAME, STEAM_ID = self.get_steamid_name(self.PROFILE_URL)
        
        AVATAR, RANKS = self.get_imgs(STEAM_ID)
        
        CURRENT_RANK = ''
        BEST_RANK = ''

        if len(RANKS) == 2:
            CURRENT_RANK, BEST_RANK = RANKS[0], RANKS[1]
        elif len(RANKS) == 1:
            CURRENT_RANK, BEST_RANK = RANKS[0], RANKS[0]
        else:   # Image with "UNRANKED" text.
            CURRENT_RANK = BEST_RANK = 'https://github.com/R37r0-Gh057/csgostats_rank_scraper/raw/main/unknown.png'

        if self.MODE == 1:
            if "unknown.png" in CURRENT_RANK:
                CURRENT_RANK = "UNKNOWN"
            if "unknown.png" in BEST_RANK:
                BEST_RANK = "UNKNOWN"

            return "Current Rank: "+CURRENT_RANK, "Best Rank: "+BEST_RANK
        else:
            return NAME, AVATAR, CURRENT_RANK, BEST_RANK

if __name__ == "__main__":
    scraper = rank_scraper(MODE=1,URL=input("Enter Steam profile URL here: "))
    print(scraper.run())
