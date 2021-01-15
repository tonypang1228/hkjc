import argparse
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description=\
         'Data processing for HKJC account html statement.')
parser.add_argument('html', type=argparse.FileType('r'),
                    help='HKJC acct statement in html format')
parser.add_argument('-o', '--output', default='csv',
                    help='output format (default: csv)')

args = parser.parse_args()
f=args.html
soup = BeautifulSoup(f.read(), 'html.parser')
#print(soup.prettify())

#### extract statement summary
summary = soup.find_all('td', class_='content')
print([s.text for s in summary])
print(summary[1].text.split(' '))
print(summary[2].text.split(' '))
#### extract data to lists


#### format lists to dataframe