import requests
import json
from bs4 import BeautifulSoup
from urllib.parse import unquote
from fastapi import APIRouter
from datetime import datetime, timedelta


router = APIRouter()

@router.get("/search/{query}")
async def search(query: str):
    query = unquote(query)
    url = f'https://indiankanoon.org/search/?formInput=doctypes:{query}'
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, 'html.parser')
    titles_and_hrefs = []
    result_titles = soup.find_all('div', class_='result_title')
    for result_title in result_titles:
        link = result_title.find('a')
        if link:
            title = link.get_text()
            href = link['href']
            titles_and_hrefs.append({
                'title': title,
                'href': href
            })
    return titles_and_hrefs

@router.get("/advsearch/")
async def advsearch(query: str, fromdate: str):
    query = unquote(query)
    date = datetime.strptime(fromdate, '%d-%m-%Y')
    date_plus_one_year = date + timedelta(days=365)
    todate = date_plus_one_year.strftime('%d-%m-%Y')
    url = f'https://indiankanoon.org/search/?formInput=doctypes:{query} fromdate:{fromdate} todate:{todate}'
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, 'html.parser')
    titles_and_hrefs = []
    result_titles = soup.find_all('div', class_='result_title')
    for result_title in result_titles:
        link = result_title.find('a')
        if link:
            title = link.get_text()
            href = link['href']
            titles_and_hrefs.append({
                'title': title,
                'href': href
            })
    return titles_and_hrefs
