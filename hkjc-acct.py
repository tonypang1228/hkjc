import argparse
from bs4 import BeautifulSoup
from datetime import datetime

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
start_date = datetime.strptime(summary[1].text.split(' ')[1], '%d/%m/%Y')
print(start_date)
end_date = datetime.strptime(summary[1].text.split(' ')[-1], '%d/%m/%Y')
print(end_date)
print(summary[2].text.split(' '))
acct = summary[2].text.split(' ')[-1]
print(acct)
output_file = acct + "-" + start_date.strftime('%Y%m%d') + "-" +\
              end_date.strftime('%Y%m%d') + "." + args.output
print(output_file)
#### extract data to lists


#### format lists to dataframe