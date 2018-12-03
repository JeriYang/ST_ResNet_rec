import pandas as pd
from datetime import datetime

def string2timestamp(strings, T=48):
    timestamps = []

    time_per_slot = 24.0 / T
    num_per_T = T // 24  #双斜杠（//）表示地板除，即先做除法（/），然后向下取整（floor）。至少有一方是float型时，结果为float型；两个数都是int型时，结果为int型。
    for t in strings:
        year, month, day, slot = int(t[:4]), int(t[4:6]), int(t[6:8]), int(t[8:])-1 #获取年，月，日和（时段信息-1）
        timestamps.append(pd.Timestamp(datetime(year, month, day, hour=int(slot * time_per_slot), minute=(slot % num_per_T) * int(60.0 * time_per_slot))))
        #转换为时间类型，年，月，日，小时，分钟
        #<class 'pandas.tslib.Timestamp'>)
        # 输出格式：2017-06-19 09:13:45
    return timestamps