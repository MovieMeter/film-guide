# Get the RottenTomatoes and Audience Rating for a movie from the RT page.

from bs4 import BeautifulSoup, SoupStrainer
import requests

from fake_useragent import UserAgent


def rotten(url):
    ua = UserAgent()
    headers = {'User-Agent': ua.chrome}


    # url = 'https://www.rottentomatoes.com/m/inception'
    r = requests.get(url, headers=headers)

    soup = BeautifulSoup(r.content, 'lxml', parse_only=SoupStrainer('div', class_='body_main container'))

    main = soup.find('div', id='mainColumn')
    # print(main)
    # exit()

    score_panel = main.find('div', id='scorePanel')

    link = score_panel.find('a', id='tomato_meter_link')
    span = link.find('span', class_='meter-value superPageFontColor')
    rating = span.text[:len(span.text)-1]

    # print(rating)

    audience = soup.find('div', class_='audience-score meter')
    value = audience.find('div', class_='meter-value')
    # print(value.text[:len(value.text)-1])
    temp1 = value.text.strip()
    audience_score = temp1[:len(temp1) - 1]
    # audience_score = value.text[:len(value.text)-1]
    # print(audience_score)
    # exit()
    meter_score = int(rating)
    a_score = int(audience_score)
    # audience_score = int(value.text[:len(value.text)-1])
    return meter_score, a_score

