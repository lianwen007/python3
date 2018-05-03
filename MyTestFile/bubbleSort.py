#冒泡排序
'''This programe is used to sort a series of numbers from little to big'''
def bubbleSort(numbers):
    for j in range(len(numbers)-1,-1,-1):#loop times
        for i in range(j):#
            if numbers[i]>numbers[i+1]:
                numbers[i],numbers[i+1] = numbers[i+1],numbers[i]
    return numbers
