import sys
import re
import datetime 

def parse_thousand(num):
    parse = num.split(',')
    new_num = ''.join(parse)
    return new_num
def con_date(date):
    parse_date = date.split('-')
    year = parse_date[0]
    month = parse_date[1]
    day = parse_date[2]
    
    if month == '01':
        month = 'Jan'
    elif month == '02':
        month = 'Feb'
    elif month == '03':
        month = 'Mar'
    elif month == '04':
        month = 'Apr'
    elif month == '05':
        month = 'May'
    elif month == '06':
        month = 'Jun'
    elif month == '07':
        month = 'Jul'
    elif month == '08':
        month = 'Aug'
    elif month == '09':
        month = 'Sep'
    elif month == '10':
        month = 'Oct'
    elif month == '11':
        month = 'Nov'
    elif month == '12':
        month = 'Dec' 
    else: 
        print('invalid date format, use yr-month-day ex.(1990-09-23)')
        exit(1)
        
    new_date = month + ' ' + day + ', ' + year
    return new_date
def date_to_dec(date):

    parse_date = re.split('\W',date)
    del parse_date[2]
    month = parse_date[0]
    day = parse_date[1]
    year = parse_date[2]
    
    if month == 'Jan':
        month = '01'
    elif month == 'Feb':
        month = '02'
    elif month == 'Mar':
        month = '03'
    elif month == 'Apr':
        month = '04'
    elif month == 'May':
        month = '05'
    elif month == 'Jun':
        month = '06'
    elif month == 'Jul':
        month = '07'
    elif month == 'Aug':
        month = '08'
    elif month == 'Sep':
        month = '09'
    elif month == 'Oct':
        month = '10'
    elif month == 'Nov':
        month = '11'
    elif month == 'Dec':
        month = '12' 
    
    return (year,month,day)
    
def cmp_date(cmp_d1,cmp_d2):
    date1 = date_to_dec(cmp_d1)
    date2 = date_to_dec(cmp_d2)
    dt1 = datetime.date(int(date1[0]),int(date1[1]),int(date1[2]))
    dt2 = datetime.date(int(date2[0]),int(date2[1]),int(date2[2]))
    if dt1 == dt2:
        return 0
    elif dt1 > dt2:
        return 1
    elif dt1 < dt2:
        return -1
    else:
        print('time compare error')
        exit(1)
    
        
def main():

    args = sys.argv
    if len(args) is not 4:
        print("usage: date-lowerbound date-upperbound commodity")
        exit(1)
    if not(args[3] == 'gold' or args[3] == 'silver'):
        print("usage: commodity must be either gold or silver")
        exit(1)
        
    date_lb = con_date(args[1])
    date_ub = con_date(args[2])
    data = None
    date_li = []
    price_li = []
    if args[3] == 'gold':
        data = open('gold.txt','r')
    else: 
        data = open('silver.txt','r')
    
    for line in data:
        temp_li = re.split(r'\s{2,}',line)
        date_li.append(temp_li[0])
        price_li.append(temp_li[1])
       
    date_li = date_li[1:len(date_li)]
    price_li = price_li[1:len(price_li)]
    
    
    bounded_li = [] #append the prices within price_li here
    
    for i,j in zip(date_li,price_li):
        
        if(cmp_date(i,date_lb) >= 0 and cmp_date(date_ub,i) >= 0):
            bounded_li.append(float(parse_thousand(j)))
       
    try:
        mean = sum(bounded_li)/len(bounded_li)
    except ZeroDivisionError:
        print('bad range or no results')
        exit(0)
    
    summation = 0
    
    for i in bounded_li:
        summation = summation + (i**2)
    
    variance = (summation/len(bounded_li)) - (mean **2)
    print('commodity: '+ args[3] + '    mean: ' + str(mean) + '  variance: ' + str(variance))
    
    

if __name__ == "__main__":
   main()    