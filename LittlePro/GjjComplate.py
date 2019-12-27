
# 额度
def cnt_avg(num=1000, init=0, chose=1):
    """
    gjj credit amount computation
    :param num: monthly payment amount
    :param init: account history amount
    :param chose: 1-show between 15W and 50W OR others-show real total amount
    :return: gjj credit amount
    """
    s = 0
    for i in range(12):
        s += (i+1) * num + init
    num = (s*15/12)
    if num < 150000:
        total_num = 150000
    elif num > 500000:
        total_num = 500000
    else:
        total_num = num
    if chose == 1:
        final = total_num
    else:
        final = num
    return final

# 还款额
def cnt_mon(num=1000, years=30, uprate=0.00, chose=1):
    if chose == 1:
        rate = 0.049 * (1+uprate)
    else:
        rate = 0.0325
    total_num = (num * (rate/12) * (1+rate/12)**(years*12))/((1+rate/12)**(years*12)-1)
    return total_num


def composite_mon(nor=100, gjj=0, uprate=0.00, years=30):
    """
    composite month repayment quota of bank
    :param nor: normal credit amount
    :param gjj: gjj credit amount
    :param uprate: normal credit uprate
    :param years: credit years
    :return: Month repayment amount
    """
    gjj_rate = 0.0325
    gjj = gjj * 10000
    nor_rate = 0.049 * (1 + uprate)
    nor = nor * 10000

    gjj_num = (gjj * (gjj_rate / 12) * (1 + gjj_rate / 12) ** (years * 12)) / ((1 + gjj_rate / 12) ** (years * 12) - 1)
    nor_num = (nor * (nor_rate / 12) * (1 + nor_rate / 12) ** (years * 12)) / ((1 + nor_rate / 12) ** (years * 12) - 1)
    total_num = nor_num + gjj_num
    return total_num
