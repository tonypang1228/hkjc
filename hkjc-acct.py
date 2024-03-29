import argparse
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd

def create_df(con):
    col = ["Ref No", "Date/Time", "Race Day", "Bet Type", "Transaction Details", "Debit", "Credit"]
    col_len = len(col)
    rl = []
    cl = []
    for c in con:
        rl.append(c)
        if len(rl) == col_len:
            cl.append(rl)
            rl = []
            continue
    
    df = pd.DataFrame(cl, columns=col)
    return df

def summary(soup):
    #### extract statement summary
    summary = soup.find_all('td', class_='content')
    #print([s.text for s in summary])
    #print(summary[1].text.split(' '))
    start_date = datetime.strptime(summary[1].text.split(' ')[1], '%d/%m/%Y')
    #print(start_date)
    end_date = datetime.strptime(summary[1].text.split(' ')[-1], '%d/%m/%Y')
    #print(end_date)
    #print(summary[2].text.split(' '))
    acct = summary[2].text.split(' ')[-1]
    #print(acct)
    output_file = acct + "-" + start_date.strftime('%Y%m%d') + "-" +\
              end_date.strftime('%Y%m%d') + "." + args.output
    #print(output_file)
    return acct, start_date, end_date, output_file

parser = argparse.ArgumentParser(description=\
         'Data processing for HKJC account html statement.')
parser.add_argument('html', type=argparse.FileType('r'),
                    help='HKJC acct statement in html format')
parser.add_argument('-o', '--output', default='csv',
                    help='output format (default: csv)')

args = parser.parse_args()
f = args.html
soup = BeautifulSoup(f.read(), 'html.parser')
#print(soup.prettify())

#### extract data to lists
con5=soup.findAll("td", class_="tableContent5")
con6=soup.findAll("td", class_="tableContent6")

c5=[co5.get_text("|") for co5 in con5]
c6=[co6.get_text("|") for co6 in con6]

#### format lists to dataframe
df5 = create_df(c5)
df6 = create_df(c6)
df = pd.concat([df5, df6], ignore_index=True)

#### Clean the Date/Time field
for i in range(len(df)):
    try:
        d = datetime.strptime(df['Date/Time'].iloc[i], "%d-%m-%Y|%H:%M")
    except:
        print("No Date/Time cleaning for record ", i)
        #d2 = datetime.strptime(df['Transaction Details'].iloc[i].split(' ')[1],
        #    "%d-%b-%Y")
        #df['Date/Time'].iloc[i] = d2
    else:    
        df['Date/Time'].iloc[i] = d
        print("Date/Time cleaning for record ", i)

print(df)
df.sort_values(by=['Ref No', 'Date/Time'], inplace=True)


#### Clean the Debit and Credit field
for i in range(len(df)):
    df["Debit"].iloc[i] = df["Debit"].iloc[i].replace("$", "").replace(",", "")
    try:
        df["Debit"].iloc[i] = float(df["Debit"].iloc[i])
    except:
        df["Debit"].iloc[i] = 0.00

    df["Credit"].iloc[i] = df["Credit"].iloc[i].replace("$", "").replace(",", "")
    try:
        df["Credit"].iloc[i] = float(df["Credit"].iloc[i])
    except:
        df["Credit"].iloc[i] = 0.00


#### Display acct statement summary
print("HKJC acct statement summary:")
acct, start_date, end_date, output_file = summary(soup)
df["Acct ID"] = acct
df = df[["Acct ID", "Ref No", "Date/Time", "Race Day", "Bet Type", "Transaction Details", "Debit", "Credit"]]
print(df)
print (start_date, " - ", end_date)
print(output_file)
df.to_csv(output_file, index=False)
