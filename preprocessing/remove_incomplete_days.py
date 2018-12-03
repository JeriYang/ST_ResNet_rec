import pandas as pd
import numpy as np
from copy import copy
import time
import h5py
from ST_ResNet.data.TaxiBJ.dataInfo import stat,load_stdata

def remove_incomplete_days(data, timestamps, T=48):
    # 删除没有48个时间戳的某一天
    days = []  # 可用日期，有些日期不包括48个时间间隙
    days_incomplete = []  # 存在问题的日期
    i = 0
    while i < len(timestamps):
        if int(timestamps[i][8:]) != 1: #开始不为1，则加1
            i = i + 1
        elif i+T-1 < len(timestamps) and int(timestamps[i+T-1][8:]) == T: #直接跳到末尾。如果数据末尾为48
            days.append(timestamps[i][:8])
            i += T
        else:
            days_incomplete.append(timestamps[i][:8])
            i += 1
    print("incomplete days: ", days_incomplete)
    days = set(days)
    idx = []
    for i, t in enumerate(timestamps):
        if t[:8] in days:
            idx.append(i)

    data = data[idx]
    timestamps = [timestamps[i] for i in idx]
    return data, timestamps   #data数据格式为：[][] 32*32 * 2； timestamps数据格式为：[]