from urllib.request import urlopen
import urllib.request, urllib.parse, urllib.error
import ssl
from bs4 import BeautifulSoup
import csv
import re

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#Getting stuff from Plane Crash Info:
url = 'http://planecrashinfo.com/database.htm'
html = urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, 'html.parser') #Main Website
csv_file = open('Plane_Crash_Info.csv','w',newline='') #For parsing and saving all the data in CSV.
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['date','VariableCategory','Variable'])
datelst = list() # List of all event wise link (for eg, for year 2010, /2010-1.htm is parsed and so on)
yearlst = list() # List of all the years
links = list() # List of all the valid html links for 2nd iteration in beautiful soup. Nested links.
a = int(input('Enter Starting year(Minimum: 1920): '))

for year in soup.find_all('a'):
    try:
        year = year.get('href',None)
        yearlst.append(year)
    except:
        pass
yearlst = yearlst[a-1920:len(yearlst)-1]
for prehtmltag in yearlst:
    prehtmllink = ''.join(re.findall('([0-9]+).htm',prehtmltag))
    yearhtmllink = f'http://planecrashinfo.com/{prehtmllink}/{prehtmllink}.htm' 
    links.append(yearhtmllink)
count = 0    
for link in links: 
    datelink = urlopen(link, context=ctx).read()
    soup1 = BeautifulSoup(datelink, 'html.parser')
    for date in soup1.find_all('a'):
        try:
            date = date.get('href',None)
            datelst.append(date)
        except:
            pass
    datelst = datelst[:len(datelst)-1]
    for htmltag in datelst:
        htmllink = re.sub('([0-9]+).htm',htmltag,links[count])
        htmlmain = urlopen(htmllink, context = ctx).read()
        souptest = BeautifulSoup(htmlmain,'html.parser')
        tag = (htmltag.split('.'))
        tag.remove('htm')
        tag = ''.join(tag)
        for content in souptest.find_all('tr'): 
            try:
                headline = content.b.text
                data = content.find('td', width = '547').text
                headline.strip()
                data.strip()
                print(headline.strip())
                print(data.strip())
            except:
                pass
            csv_writer.writerow([''.join(tag),headline,data])
    datelst.clear()
    count = count + 1         
csv_file.close()