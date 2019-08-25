"""
Produces a CSV file of WhatsApp message sentiment by week.
"""

from whatsapplog import WhatsAppLog
import boto3, json, sys, time
from datetime import datetime, timedelta

comprehend = boto3.client('comprehend')

parser = WhatsAppLog("chat.txt")
parser.parse()

start = datetime(2017, 9, 21, 16, 19).replace(hour=0, minute=0, second=0)
end = start
limit = datetime(2018, 1, 22, 8, 20)

with open('sentiment.csv','w') as f:
    f.write("Week beginning,Mixed,Negative,Neutral,Positive\n")

while end < limit:
    end = start.replace(hour=23, minute=59, second=59) + timedelta(days=7)
    
    results = parser.filter(afterdatetime = start, beforedatetime = end)
    
    i = 0
    j = 0
    k = 0
    week_sums = {
            "Mixed": 0,
            "Negative": 0,
            "Neutral": 0,
            "Positive": 0
        }
    
    text_list = []
    text_lists = [] # Batches for < 25 for stupid Amazon
    for result in results:
        i += 1
        j += 1
        text = result["message"].decode("utf-8")
        print("\rListing {}/{}".format(i, len(results)), end="")
        if len(text) > 0 and text != "<Media omitted>":
            k += 1
            if j < 20:
                text_list.append(result["message"].decode("utf-8"))
            else:
                text_list.append(result["message"].decode("utf-8"))
                text_lists.append(text_list)
                text_list = []
                j = 0
        
    text_lists.append(text_list)
    
    sentiment_lists = []
    print("\nSending for sentiment calculations...")
    
    for text_list in text_lists:
        if len(text_list) > 0:
            sentiment_lists.append(comprehend.batch_detect_sentiment(TextList = text_list, LanguageCode='en'))
    
    print("Processing response...")
    for sentiments in sentiment_lists:
        for sentiment in sentiments["ResultList"]:
            for score in sentiment["SentimentScore"]:
                 week_sums[score] += sentiment["SentimentScore"][score]

    for score in week_sums:
        if k > 0:
            week_sums[score] = week_sums[score] / k
        else:
            print("ERROR1")
            print(week_sums)
            break

    with open('sentiment.csv','a') as f:
        f.write("{},{},{},{},{}\n".format(
            start.strftime("%Y-%m-%d"),
            week_sums["Mixed"],
            week_sums["Negative"],
            week_sums["Neutral"],
            week_sums["Positive"],
        )) 
    
    start = end + timedelta(seconds=1)
    time.sleep(0.5)
    
