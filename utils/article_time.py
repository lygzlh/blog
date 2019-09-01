import time
def time_set(article):
    for i in article:
        timeArray = time.localtime(i.date)
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        i.date = otherStyleTime