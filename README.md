# csgostats_rank_scraper

[![Selenium](https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=Selenium&logoColor=white)](https://github.com/alexandresanlim/Badges4-README.md-Profile#-frameworks--library-) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://makeapullrequest.com)

# Table of contents:
  - [Introduction](#introduction)
  - [Setup](#setup)
  - [Usage](#usage)
  - [How to load as module](#how-to-load-as-module)

# Introduction:
This script is made in python, which uses the selenium webdriver to scrape a player's competitive rank information from [csgostats](https://csgostats.gg).

The script can be used in two ways:
  * You can get a player's Steam profile name, current rank icon URL, best rank icon URL for using in your discord/TG/etc bots.
<p align="center">OR</p>
  
  * You can just get the current and best ranks information in plain-text for local usage.
 
# Setup:
* Install the selenium library: `pip install selenium`
* Download the suitable chromedriver according to your chrome browser version from [here](https://chromedriver.chromium.org/downloads)

# Usage:
* Run the script once to enter the path to your driver, or manually change the path in `driver_path.txt`.
* To run: `python rank_scrape.py`

# How to load as module:
You can use it in your Discord or other bots by loading it as a module like this:
```Python

import rank_scrape

scraper = rank_scrape.rank_scraper(MODE=0,URL=steam_profile_url_here)

player_name, player_avatar_url current_rank_icon_url, best_rank_icon_url = scraper.run()
```
You will get the player's steam profile name, avatar image URL, current rank's icon URL, best rank's icon URL.
