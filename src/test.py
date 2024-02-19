from bs4 import BeautifulSoup
import requests
#send req to the url and get the html content
url = 'https://indiankanoon.org/search/?formInput=doctypes:constitution-amendments%20fromdate:1-1-1987%20todate:%2031-12-1987'
html_content = requests.get(url).text

soup = BeautifulSoup(html_content, 'html.parser')
titles_and_hrefs = []
# Find all elements with class 'result_title'
result_titles = soup.find_all('div', class_='result_title')

# Extract the href attribute from each result_title
for result_title in result_titles:
    link = result_title.find('a')
    if link:
        title = link.get_text()
        href = link['href']
        titles_and_hrefs.append({
            'title': title,
            'href': href
        })
print(titles_and_hrefs)