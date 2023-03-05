import asyncio
import time
import aiohttp
from bs4 import BeautifulSoup as bs
import random
import os
from multiprocessing import Pool, cpu_count
import  requests
from db import Database
import csv


os.system("python3 Users.py")
db = Database('dizainiri.db')
def random_user():
    users = []
    f = open('User_Agent.txt')
    for line in f:
        users.append(line)
    random_index = random.randint(0, len(users) - 1)
    header = {
        'accept': '*/*',
        'user-agent': users[random_index].strip()}
    return header

async def get_user_data(url, session, link):
    async with session.get(url=url, headers=random_user()) as respons:
        html = bs(await respons.text(), 'lxml')
        all_page_users = html.find_all('div', class_='user-preview user-preview__default')
        for user in all_page_users:
            link.append(user.find('a', class_='user-preview_name').get('href'))
        return link

async def task_data():
    link = []
    url = 'https://www.inmyroom.ru/profi/page/1'
    async with aiohttp.ClientSession() as session:
        all_page = None
        while all_page == None:
            r = await session.get(url=url, headers=random_user())
            html = bs(await r.text(), 'lxml')
            try:
                all_page = round(int(html.find('h1', class_='b-PageTitle').text.split()[0]) / 20)
            except AttributeError:
                time.sleep(5)
        tasks = []
        for page in range(1, all_page + 1):
            url = f'https://www.inmyroom.ru/profi/page/{page}'
            task = asyncio.create_task(get_user_data(url, session, link))
            tasks.append(task)
        await asyncio.gather(*tasks)
    return link

def pars(url):
    data = []
    r = requests.get(url=url, headers=random_user())
    html = bs(r.text, 'lxml')
    social_url = ''
    try:
        name = html.find('h1', class_='s-UserProfile_b-Header_title').text
    except AttributeError:
        name = 'None'
    try:
        citi = html.find('p', class_='s-UserProfile_b-Header_subtitle').text.split('/')[1]
    except (IndexError, AttributeError):
        citi = 'None'
    try:
        tel = html.find('a', class_='__withIcon __phone').get('href').strip().replace('tel:', '')
    except AttributeError:
        tel = 'None'
    try:
        socials = html.find('ul', class_='s-UserProfile_b-Socials').find_all('li')
        for iten in socials:
            social_urls = str(iten.find('a').get('href') + '; ')
            social_url += social_urls
    except AttributeError:
        social_url = 'None'
    portfolios = url + '/portfolios'
    if (tel == 'None') and (social_url == 'None'):
        pass
    else:
        data.append(
            {
                'Имя': name,
                'Город': citi,
                'Телефон': tel,
                'Url соцсетей': social_url,
                'Порфолио': portfolios
            }
        )
        db.add_user([name,citi,tel,social_url,portfolios])
    return data
def main():
    while True:
        time.sleep(7200)
        if os.path.isfile('backup.csv'):
            os.remove('backup.csv')
        with Pool(cpu_count()) as p:
            for user in p.map(pars, asyncio.run(task_data())):
                try:
                    with open('backup.csv', 'a') as f:
                        writer = csv.writer(f)
                        writer.writerow([user[0]['Имя'],
                                     user[0]['Город'],
                                     user[0]['Телефон'],
                                     user[0]['Url соцсетей'],
                                     user[0]['Порфолио']])
                except IndexError:
                    continue



if __name__ == '__main__':
    main()



