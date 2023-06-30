import os
import time
from urllib.request import urlretrieve

import pandas as pd
# import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from tqdm import tqdm
    

def download_phf_gamebooks(season:int):
    """
    
    """
    print(f'\nGetting the PHF schedule for {season}.')
    schedule_url = f"https://raw.githubusercontent.com/sportsdataverse/fastRhockey-data/main/phf/schedules/csv/phf_schedule_{season}.csv"
    schedule_df = pd.read_csv(schedule_url)

    try:
        os.mkdir(f'gamebooks/{season}')
    except:
        print(f'Directory to hold {season} gamebooks has already been created.')

    print('Gathering a list of PHF game IDs.')
    game_ids_arr = schedule_df['game_id'].to_numpy()
    print('Starting up the webdriver.')
    driver = webdriver.Chrome()

    print('Processing games.')
    for game_id in tqdm(game_ids_arr):
        game_url = f"https://www.premierhockeyfederation.com/stats#/100/game/{game_id}"

        driver.get(game_url)
        time.sleep(10)

        soup = BeautifulSoup(driver.page_source,features='lxml')

        gamebook_url = soup.find('a',{'target':'_blank','aria-label':'Gamesheet'}).get('href')
        
        urlretrieve(gamebook_url,filename=f'gamebooks/{season}/{game_id}.pdf')
        time.sleep(3)

if __name__ == "__main__":
    for i in range(2023,2024):
        download_phf_gamebooks(i)
