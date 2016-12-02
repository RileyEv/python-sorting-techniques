# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from Queue import Queue
from threading import Thread
from heapq import merge
import timeit
import random
import csv
import numpy as np


def mergeSort(m):
    if len(m) <= 1:
        return m

    middle = len(m) // 2
    left = m[:middle]
    right = m[middle:]

    left = mergeSort(left)
    right = mergeSort(right)
    return list(merge(left, right))


def quickSort(arr):
    less = []
    pivotList = []
    more = []
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[0]
        for i in arr:
            if i < pivot:
                less.append(i)
            elif i > pivot:
                more.append(i)
            else:
                pivotList.append(i)
                less = quickSort(less)
                more = quickSort(more)
        return less + pivotList + more


def insertionSort(alist):
    for index in range(1, len(alist)):
        currentvalue = alist[index]
        position = index
        while position > 0 and alist[position - 1] > currentvalue:
            alist[position] = alist[position - 1]
            position = position - 1
        alist[position] = currentvalue
    return alist


def bubbleSort(arr):
    sorted = False
    while not sorted:
        sorted = True  # Assume the list is now sorted
        for n in range(0, len(arr) - 1):
            if arr[n] > arr[n + 1]:
                sorted = False  # We found two elements in the wrong
                arr[n + 1], arr[n] = arr[n], arr[n + 1]
    return arr


def pythonSort(arr):
    return sorted(arr)


def rileyBubbleSort(arr):
    sorted = False
    count = len(arr)
    while not sorted:
        sorted = True
        count -= 1
        if count > 0:
            for n in range(0, count):
                if arr[n] > arr[n + 1]:
                    sorted = False
                    arr[n + 1], arr[n] = arr[n], arr[n + 1]
    return arr


results = {
}


def sortData(q):  # main sorting function
    while True:
        arr = q.get()
        start_time = timeit.default_timer()
        bubble = bubbleSort(arr)
        bubble_time = timeit.default_timer() - start_time
        start_time = timeit.default_timer()
        merge = mergeSort(arr)
        merge_time = timeit.default_timer() - start_time
        start_time = timeit.default_timer()
        insertion = insertionSort(arr)
        insertion_time = timeit.default_timer() - start_time
        start_time = timeit.default_timer()
        quick = quickSort(arr)
        quick_time = timeit.default_timer() - start_time
        start_time = timeit.default_timer()
        python = pythonSort(arr)
        python_time = timeit.default_timer() - start_time
        start_time = timeit.default_timer()
        riley_bubble = rileyBubbleSort(arr)
        riley_bubble_time = timeit.default_timer() - start_time
        if quick == bubble and quick == merge and python == riley_bubble and quick == insertion:
            results[len(arr)].append({
                'bubble': bubble_time,
                'merge': merge_time,
                'insertion': insertion_time,
                'quick': quick_time,
                'python': python_time,
                'riley_bubble': riley_bubble_time
            })
        q.task_done()


q = Queue(maxsize=0)
num_threads = 4  # choose an appropriate number of threads for your computer

for i in range(num_threads):
    worker = Thread(target=sortData, args=(q,))
    worker.setDaemon(True)
    worker.start()


for a in range(100, 1001, 100):
    results[a] = []

for i in range(10000):
    length = random.randrange(100, 1100, 100)
    q.put([random.randrange(0, length, 1) for x in range(length)])

q.join()

averages = {}

print(results)

for k, v in results.iteritems():
    bubble_total = 0
    bubble_list = []
    merge_total = 0
    merge_list = []
    insertion_total = 0
    insertion_list = []
    quick_total = 0
    quick_list = []
    python_total = 0
    python_list = []
    riley_bubble_total = 0
    riley_bubble_list = []
    n = 0
    for i in v:
        n += 1
        bubble_total += i['bubble']
        bubble_list.append(i['bubble'])
        merge_total += i['merge']
        merge_list.append(i['merge'])
        insertion_total += i['insertion']
        insertion_list.append(i['insertion'])
        quick_total += i['quick']
        quick_list.append(i['quick'])
        python_total += i['python']
        python_list.append(i['python'])
        riley_bubble_total += i['riley_bubble']
        riley_bubble_list.append(i['riley_bubble'])
    averages[k] = {
        'bubble': bubble_total / float(n),
        'bubble_std': np.std(np.array(bubble_list)),
        'merge': merge_total / float(n),
        'merge_std': np.std(np.array(merge_list)),
        'insertion': insertion_total / float(n),
        'insertion_std': np.std(np.array(insertion_list)),
        'quick': quick_total / float(n),
        'quick_std': np.std(np.array(quick_list)),
        'python': python_total / float(n),
        'python_std': np.std(np.array(python_list)),
        'riley_bubble': riley_bubble_total / float(n),
        'riley_bubble_std': np.std(np.array(riley_bubble_list)),
    }

print(averages)

data = [
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
]

for k, v in sorted(averages.iteritems()):
    data[0].append(k)
    data[1].append(v['bubble'])
    data[2].append(v['bubble_std'])
    data[3].append(v['merge'])
    data[4].append(v['merge_std'])
    data[5].append(v['insertion'])
    data[6].append(v['insertion_std'])
    data[7].append(v['quick'])
    data[8].append(v['quick_std'])
    data[9].append(v['python'])
    data[10].append(v['python_std'])
    data[11].append(v['riley_bubble'])
    data[12].append(v['riley_bubble_std'])

with open('averages.csv', 'w') as f:
    csvfile = csv.writer(f)
    for i in data:
        csvfile.writerow(i)
