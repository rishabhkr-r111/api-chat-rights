import requests
import json
from bs4 import BeautifulSoup
from urllib.parse import unquote
from fastapi import APIRouter

router = APIRouter()

@router.get("/years/{law}")
async def get_years(law: str):
    query = unquote(law)
    url = f'https://indiankanoon.org/browse/{law}'
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, 'html.parser')
    years = []
    year_links = soup.select('.browselist a')
    for result_title in year_links:
        year = result_title.get_text()
        years.append(year)
    return years
