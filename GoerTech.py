import http.client,urllib,urllib.request
import time
import sys, json

price = 0.0
weekDay = 1
timeNow = 0
priceUpload = False

#get the weekday of the day time.localtime()[6]( 0~6 ) refer to Monday to Saturday.
def getWeekDay():
    return time.localtime()[6]+1

#get the time now return hour*100+minute cause it is easy to deal with integer
def getTime():
    return ((time.localtime()[3]+8)%24)*100 + time.localtime()[4]
    
#get goerTech stock price from BaiduAPI
def getPrice():
    url = 'http://apis.baidu.com/apistore/stockservice/stock?stockid=sz002241&list=1'
    req = urllib.request.Request(url)
    req.add_header("apikey", "101698c2697998bf50dfb7b4bd8ca257")
    resp = urllib.request.urlopen(req)
    content = resp.read()
    if(content):
        data = json.loads(content.decode())
        return data["retData"]["stockinfo"][0]["currentPrice"]

#update price to thingspeak.com Channel raspberrypi_test field2
def updateTothingspeak():
    params = urllib.parse.urlencode({'field2':price,'key':'9Y5MLA363UBKJWON'})
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    conn = http.client.HTTPConnection("api.thingspeak.com:80")
    conn.request("POST", "/update", params, headers)
    response = conn.getresponse()
    print(response.status)
    data = response.read()
    conn.close()

#sleep for 16 seconds (api limit of 15 secs)
if __name__ == "__main__":
    while True:
        weekDay = getWeekDay()
        timeNow = getTime()
        #if the day is a workday
        if(weekDay<6):
            #if the time between 9:30~11:30am or 13:00~15:00pm
            if((timeNow>930 and timeNow<1130) or (timeNow>1300 and timeNow<1500)):
                price = getPrice()
                updateTothingspeak()
        time.sleep(20)
