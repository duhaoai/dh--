import pandas as pd
import math
import matplotlib.pyplot as plt
from scipy import stats

Code=[]
Name=[]
Time=[]
StartValue=[]
EndValue=[]
TurnOverValue=[]
times=[]
time_aves = []

class time:
    def __init__(self,t):
        self.year=t[0]
        self.month=t[1]
        self.day=t[2]

def read_csv():
    csv_file=open(r"600009.SH.CSV")
    csv=pd.read_csv(csv_file)
    for i in csv.values:
        Code.append(i[0])
        Name.append(i[1])
        Time.append(i[2])
        StartValue.append(i[3])
        EndValue.append(i[7])
        TurnOverValue.append(i[9])
        #代码、简称，日期，开盘价(元)，收盘价(元)，成交金额(元)
def time_spilt():
    for i in range(len(Time)):
        a=Time[i].split("-")
        a=time(a)
        times.append(a)

def calulate():
    ave_start=0
    ave_end=0
    sum=0
    num_start=0
    num_end=0
    cur_year=times[0].year
    cur_month=times[0].month
    for i in range(len(times)):
        if(cur_year == times[i].year and cur_month==times[i].month):
            if(math.isnan(StartValue[i])==False):
                ave_start=ave_start+StartValue[i]
                num_start=num_start+1
            if (math.isnan(EndValue[i]) == False):
                ave_end=ave_end+EndValue[i]
                num_end=num_end+1
            if(math.isnan(TurnOverValue[i])==False):
                sum=sum+TurnOverValue[i]
        else:
            time_ave=[]
            ave_start=ave_start/num_start
            ave_end=ave_end/num_end
            num_start=0
            num_end=0
            a=[cur_year, cur_month, ave_start, ave_end, sum]
            time_aves.append(a)
            cur_year=times[i].year
            cur_month=times[i].month
            ave_start=0
            ave_end=0
            sum=0
def draw():
    time=[]
    ave_end=[]
    ave_start=[]
    sum=[]
    for i in time_aves:
        time.append(i[0]+"."+i[1])
        ave_start.append(i[2])
        ave_end.append(i[3])
        sum.append(i[-1])
    plt.figure(figsize=(20,20))
    plt.xlabel("time")
    plt.ylabel("value")
    plt.plot(time,ave_start,label='start')
    plt.plot(time,ave_end,alpha=0.5,label="end")
    #plt.plot(time,sum)
    plt.legend()
    plt.show()
    plt.savefig("result.jpg")
def Normal_distribution():
    sum=[]
    for i in time_aves:
        sum.append(i[-1])
    df = pd.DataFrame(sum, columns=['value'])
    u = df['value'].mean()  # 计算均值
    std = df['value'].std()  # 计算标准差
    [D,P]=stats.kstest(df['value'], 'norm', (u, std))
    print(P)
    if(P>0.05):
        print("符合正态分布")
    else:
        print("不符合正态分布")
    # .kstest方法：KS检验，参数分别是：待检验的数据，检验方法（这里设置成norm正态分布），均值与标准差
    # 结果返回两个值：statistic → D值，pvalue → P值
    # p值大于0.05，为正态分布
if __name__=="__main__":
    read_csv()
    time_spilt()
    calulate()
    draw()
    Normal_distribution()
    #print(time_aves[0][0]+"."+time_aves[0][1])

