from bs4 import BeautifulSoup as bs
import requests
import os
import urllib3



def main():
    urllib3.disable_warnings()
    agent = []
    with open('User_Agent.txt', 'r') as f:
        for line in f:
            agent.append(line)
    if int(len(agent)) > 36:
        os.remove('User_Agent.txt')
    url = 'https://generatefakename.com/user-agent'
    r = requests.get(url=url, verify=False).text
    html = bs(r, 'lxml')
    users = html.find_all('div', class_='panel-body')
    for user in users:
        with open('User_Agent.txt', 'a') as f:
            f.write(user.find('h3').text + '\n')


if __name__ == '__main__':
    main()