
# 额度
def cnt_avg(num=1000, init=0):
    s = 0
    for i in range(12):
        s += (i+1) * num + init
    print(s*15/12)

# 还款额
def cnt_mon(num=1000, years=30, uprate=0.00, chose=1):
    if chose == 1:
        rate = 0.049 * (1+uprate)
    else:
        rate = 0.0325
    total_num = (num * (rate/12) * (1+rate/12)**(years*12))/((1+rate/12)**(years*12)-1)
    return total_num
