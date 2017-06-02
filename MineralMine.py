from datetime import datetime

from lxml import html
import requests

import urllib2

from bs4 import BeautifulSoup

import re
#use urllib2 & beautifulsoup to datamine 
def printf(row):
    print "<%s %s>"%(row.tag, row.attrib)

def webscrape(url_address):
    url = url_address
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
    req = urllib2.Request(url,headers = hdr)

    try:
		response = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
		print e.fp.read()
    
    html = response.read()
    response.close()
    soup = BeautifulSoup(html,"lxml")
    table = soup.find('table',class_="genTbl closedTbl historicalTbl")
    tbl_header = table.find('thead')
    tbl_header_li = tbl_header.get_text().split()[0:2]
    enc_htbl_li = [s.encode('ascii') for s in tbl_header_li] 
    #print(enc_htbl_li)
    #[x.encode('UTF8') for x in tbl_header_li]	
    tbl_body_li = []
    tbl_body = table.find('tbody')
    rows = tbl_body.find_all('tr')
    for row in rows:
        col = row.find_all('td')
        col = [c.text.strip() for c in col]
        tbl_body_li.append(col[0:2])
        
    enc_btbl_li = [[s.encode('ascii') for s in list] for list in tbl_body_li]
    #print(enc_btbl_li)
    #new_soup = BeautifulSoup(html,"lxml")
    summary_tbl = soup.find('table',id="placehereresult2")
    tbl_footer = summary_tbl.find('tbody')
    tbl_footer_li = tbl_footer.get_text().split()
    enc_ftbl_li = [s.encode('ascii') for s in tbl_footer_li]
    #print(enc_ftbl_li)
    return (enc_htbl_li,enc_btbl_li,enc_ftbl_li)
    

        
def main():
    url_gold = 'https://www.investing.com/commodities/gold-historical-data'
    url_silver = 'https://www.investing.com/commodities/silver-historical-data'
    gold_tup = webscrape(url_gold)
    silv_tup = webscrape(url_silver)
    
    gold_outfile = 'gold.txt'
    silver_outfile = 'silver.txt'
    wr_gold = open (gold_outfile , 'w')
    wr_silver = open(silver_outfile, 'w')
    
    #gold write
    for i in gold_tup[0]:
        wr_gold.write(i)
        wr_gold.write('             ')
    wr_gold.write('\n')
    for i in gold_tup[1]:
       
        for j in i:
            wr_gold.write(j)
            wr_gold.write('     ')
        wr_gold.write('\n')
    
    """for i in gold_tup[2]:
        wr_gold.write(i)
        wr_gold.write('|')"""
        
    #silver write    
    for i in silv_tup[0]:
        wr_silver.write(i)
        wr_silver.write('             ')
    wr_silver.write('\n')
    for i in silv_tup[1]:
       
        for j in i:
            wr_silver.write(j)
            wr_silver.write('     ')
        wr_silver.write('\n')   
    
    """for i in silv_tup[2]:
        wr_silver.write(i)
        wr_silver.write('|')"""

if __name__ == "__main__":
   main()    