import random
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
    
arr = [random.randrange(0,100,1) for x in range(100)]

print(arr)
print(rileyBubbleSort(arr))
