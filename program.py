# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from Queue import Queue
from threading import Thread
from heapq import merge
import timeit
import random


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
        if quick == bubble and quick == merge and quick == insertion:
            results[len(arr)].append({
                'bubble': bubble_time,
                'merge': merge_time,
                'insertion': insertion_time,
                'quick': quick_time,
            })
        q.task_done()

q = Queue(maxsize=0)
num_threads = 5

for i in range(num_threads):
    worker = Thread(target=sortData, args=(q,))
    worker.setDaemon(True)
    worker.start()


for a in range(100, 1001, 100):
    results[a] = []
    for n in range(1000):
        q.put([random.randrange(0, 100, 1) for x in range(a)])

q.join()

averages = {}

for k, v in results.iteritems():
    bubble_total = 0
    merge_total = 0
    insertion_total = 0
    quick_total = 0
    n = 0
    for i in v:
        n += 1
        bubble_total += i['bubble']
        merge_total += i['merge']
        insertion_total += i['insertion']
        quick_total += i['quick']
    averages[k] = {
        'bubble': bubble_total / float(n),
        'merge': merge_total / float(n),
        'insertion': insertion_total / float(n),
        'quick': quick_total / float(n),
    }

print(averages)

