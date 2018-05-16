#冒泡排序
'''This programe is used to sort a series of numbers from little to big'''
def bubbleSort(numbers):
    for j in range(len(numbers)-1,-1,-1):#loop times
        for i in range(j):#
            if numbers[i]>numbers[i+1]:
                numbers[i],numbers[i+1] = numbers[i+1],numbers[i]
    return numbers


# list嵌套dict排序
a = [{'name':'asd','age':23},{'name':'bbb','age':24},{'name':'aab','age':55},{'name':'ttt','age':22},]
a.sort(key=lambda x:(x['name'],x['age']))
a.sort(key=lambda x: x['name'])
