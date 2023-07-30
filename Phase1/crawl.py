# Farzaneh Soltanzadeh

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import time


options = Options()
# options.headless = True
options.add_argument("--lang=en")
driver = webdriver.Chrome(options=options)

driver.get("https://www.imdb.com/chart/top/?ref_=nv_mv_250")
movies_urls = list(map(lambda u: u.get_attribute('href') ,driver.find_elements(By.CSS_SELECTOR, '.titleColumn a')))
movies, persons = [], [] 



for i in range(len(movies_urls)): # top 250 movies
    driver.get(movies_urls[i])
    table_movie = {}

    movie_id = movies_urls[i].split('/')[4].replace('tt', '')
    
    title = driver.find_element(By.CSS_SELECTOR, '.sc-52d569c6-0 h1 span').text
    
    ypr = [li.text for li in driver.find_elements(By.CSS_SELECTOR, '.sc-52d569c6-0 ul li')]
    year, parental_guide, runtime = ypr if len(ypr) == 3 else (ypr[0], None, ypr[1])
    
    if not parental_guide or parental_guide.lower() in ('not rated', 'blank'):
        parental_guide = 'Unrated'

    if 'm' in runtime and 'h' in runtime:
        hour, minu = map(int, runtime.replace('h', '').replace('m', '').split())
    elif 'h' in runtime:
        hour, minu = int(runtime.replace('h', '')), 0
    elif 'm' in runtime:
        hour, minu = 0, int(runtime.replace('m', ''))
    runtime = 60 * hour + minu
    
    genres = [genre.text for genre in driver.find_elements(By.CSS_SELECTOR, '.ipc-chip-list__scroller a')]
    
    dws = driver.find_elements(By.CSS_SELECTOR, '.sc-52d569c6-3 > div > ul > li')
    direcors, writers, stars = [[name.text for name in row.find_elements(By.CSS_SELECTOR, '.ipc-metadata-list-item__content-container ul li')] for row in dws]
    
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # time.sleep(6)
    # storyline = driver.find_element(By.CSS_SELECTOR, '.sc-fa971bb0-0 > div > div > div').text
    
    gross_us_canada = None
    for box_office in driver.find_elements(By.CSS_SELECTOR, '.VdkJY.ipc-metadata-list--base li'):
        if box_office.find_element(By.CSS_SELECTOR, 'span').text == 'Gross US & Canada':
            gross_us_canada = int(box_office.text.split('\n')[1].replace('$', '').replace(',', ''))

    
    table_movie['id'] = movie_id
    table_movie['title'] = title
    table_movie['year'] = year
    table_movie['parental_guide'] = parental_guide
    table_movie['runtime'] = runtime
    table_movie['genre'] = genres
    table_movie['directore'] = direcors
    table_movie['writer'] = writers
    table_movie['star'] = stars
    # table_movie['storyline'] = storyline
    table_movie['gross_us_canada'] = gross_us_canada
    movies.append(table_movie)

    for name in driver.find_elements(By.CSS_SELECTOR, '.sc-52d569c6-3 > div > ul > li .ipc-metadata-list-item__content-container ul li'):
        persons.append({'name': name.text, 'id': name.find_element(By.TAG_NAME, 'a').get_attribute('href').split('/')[4].replace('nm', '')})

    print(f'movie {i+1}: Done.')
    


driver.quit()

pd.DataFrame(movies).to_json('imdb_250_movies.json', orient='records')
pd.DataFrame(persons).to_json('imdb_persons_id.json', orient='records')

