import subprocess
import warnings

import pandas as pd
import requests
import win32com.client
from bs4 import BeautifulSoup

warnings.simplefilter(action = 'ignore', category = FutureWarning)

no_articles = 35
header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'} #emulate browser
data = pd.DataFrame(columns = ['Source', 'Article', 'Text'])
source_list = []
article_list = []
text_list = []

sources = [
    'https://www.manchestereveningnews.co.uk/news/uk-news/',
    'https://www.bbc.co.uk/news/uk'
]

link_classes = [
    'headline',
    'gs-c-promo-heading'
]

removable_substring = [
    'https://www.manchestereveningnews.co.uk/news/uk-news/',
    '/news/uk'
]

try:
    for i in range(len(sources)):
        source = sources[i]
        html_class = link_classes[i]

        site_response = requests.get(source, headers = header)
        site_content = BeautifulSoup(site_response.content, 'html.parser')
        site_articles = site_content.find_all('a', {'class':  html_class})

        for j in range(no_articles):
            article_url = site_articles[j].get('href').replace(removable_substring[i], '')
            full_url = str(source + article_url)
            article_response = requests.get(full_url, headers = header)
            article_soup = BeautifulSoup(article_response.content, 'html.parser')

            article_text = ''
            article_paragraphs = article_soup.find_all('p')
            for paragraph in article_paragraphs:
                article_text += paragraph.text

            article_title = article_soup.find('h1').text
                
            source_list.append(source)
            article_list.append(article_title)
            text_list.append(article_text)

    data['Source'] = source_list
    data['Article'] = article_list
    data['Text'] = text_list           
    data.to_csv('D:/OneDrive/Desktop/articles_dirty.csv', index = False)
    print('Scraping complete!')

    #run Cleaner.py to clean the data
    subprocess.run(['python', 'D:/OneDrive/Desktop/Cleaner.py'])

    #automatically display the results in Excel for testing
    #excel = win32com.client.Dispatch('Excel.Application')
    #excel.Visible = True
    #excel.WindowState = -4137
    #workbook = excel.Workbooks.Open(r'D:/OneDrive/Desktop/articles_clean.csv')
    #worksheet = workbook.ActiveSheet
    #worksheet.Columns.AutoFit()
    #win32com.client.Dispatch("WScript.Shell").AppActivate(excel.Caption)

    #run Analyser.py to generate an analysis of the collected data
    subprocess.run(['python', 'D:/OneDrive/Desktop/Analyser.py'])

    #run Plotter.py to generate an analysis of the collected data
    subprocess.run(['python', 'D:/OneDrive/Desktop/Plotter.py'])
except:
    print('Scraping failed!')
    exit()