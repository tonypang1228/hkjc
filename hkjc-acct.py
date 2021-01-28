import argparse
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd

def create_df(con):
    col = ["Ref No", "Date/Time", "Race Day", "Bet Type", "Transaction Details", "Debit", "Credit"]
    df = pd.DataFrame(columns=col)
    return df


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
con5=soup.findAll("td", class_="tableContent5")
con6=soup.findAll("td", class_="tableContent6")

c5=[co5.text for co5 in con5]
c6=[co6.text for co6 in con6]

print(c5)
print(c6)
print(len(c5))
print(len(c6))
#### format lists to dataframe
df = create_df(con5)
print(df)