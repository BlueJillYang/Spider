from datetime import datetime

stime = datetime(2018,10,26,10,5,0)

while True:
    now = datetime.now()
    if stime < now:
        print('times up')
        break
    else:
        pass
