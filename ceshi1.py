import multiprocessing
import time

def worker(d, key, value):
    # print key,value
    d[key] = value

if __name__ == '__main__':
    mgr = multiprocessing.Manager()
    d = mgr.dict()
    jobs = [ multiprocessing.Process(target=worker, args=(d, i, i*2))
             for i in range(10) 
             ]
    # print jobs
    for j in jobs:
        j.start()
    for j in jobs:
        j.join()
    print ('Results:' )
    for key , value in dict(d).items():
       print key , value