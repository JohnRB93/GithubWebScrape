from bs4 import BeautifulSoup
from cleantext import clean
import requests
import csv
import xlwings

xlwings.App(visible=False)

def start_csv_file():
    filename = "C:/Users/john_/projects/GithubWebScrape/trending_repositories.csv"
    csv_file = open(file=filename, mode='w', newline='')
    writer = csv.writer(csv_file)
    headers = ('Repository', 'Description', 'Primary Programming Language', 'Stargazers', 'Forks', 'Stared Today')
    writer.writerow(headers)
    csv_file.close()
    
def append_to_csv(link, description, prog_lang, stars, forks, stars_today):
    csv_file = open(file='trending_repositories.csv', mode='a', newline='')
    writer = csv.writer(csv_file)
    row = (link, description, prog_lang, stars, forks, stars_today)
    writer.writerow(row)
    csv_file.close()

url = 'https://github.com/trending?since=daily&spoken_language_code=en'
html_text = requests.get(url).text
soup = BeautifulSoup(html_text, 'lxml')
repositories = soup.find_all('article', {'class': 'Box-row'})
start_csv_file()

for repository in repositories:
    try:
        url_prefix = 'https://github.com'
        link = url_prefix + repository.h2.a['href']
        description = repository.find('p', class_='col-9 color-fg-muted my-1 pr-4').text.strip()
        description = clean(description, no_emoji=True, lower=False,)
        prog_lang = repository.find('span', {'itemprop': 'programmingLanguage'}).text.strip()
        stars_forks = repository.find_all('a', class_='Link Link--muted d-inline-block mr-3')
        stars = stars_forks[0].text.strip()
        forks = stars_forks[1].text.strip()
        stars_today = repository.find('span', class_='d-inline-block float-sm-right').text.strip()
        sub_stars_today = stars_today[0: stars_today.find(' ')]
    except:
        print('\n\nInsufficient data.. Skipping repository.\n')
    else:
        print('\n'+link)
        print('Discription: ' + description)
        print('Primary Programming Language: ' + prog_lang)
        print('Stargazers: ' + stars)
        print('Fork: ' + forks)
        print('Stars Gained Today: ' + sub_stars_today)
        append_to_csv(link, description, prog_lang, stars, forks, sub_stars_today)

wb = xlwings.Book('trending_repositories.xlsm')
macro = wb.macro('Sheet1.ImportCSVData')
macro()
wb.save()
wb.close()