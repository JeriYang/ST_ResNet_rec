import pandas as pd
import numpy as np
from ST_ResNet.utils import string2timestamp


class STMatrix(object):
    """docstring for STMatrix"""

    def __init__(self, data, timestamps, T=48, CheckComplete=True):
        super(STMatrix, self).__init__()
        assert len(data) == len(timestamps) #如果数据量和时间戳数量不等，则断点
        self.data = data
        self.timestamps = timestamps
        self.T = T
        self.pd_timestamps = string2timestamp(timestamps, T=self.T) # 转化为时间（年，月，日，小时，分钟）
        # 输出格式：2017-06-19 09:13:45
        if CheckComplete:  # 用于检测完整性
            self.check_complete()
        # index
        self.make_index()

    def make_index(self):
        self.get_index = dict()  # 转化为字典
        # get_index['2013-07-01 00:00:00'] = 0; get_index['2013-07-01 00:30:00'] = 1
        for i, ts in enumerate(self.pd_timestamps): # enumerate用于为每个日期添加索引
            self.get_index[ts] = i

    def check_complete(self):
        missing_timestamps = []
        offset = pd.DateOffset(minutes=24 * 60 // self.T)
        pd_timestamps = self.pd_timestamps
        i = 1
        while i < len(pd_timestamps):
            if pd_timestamps[i-1] + offset != pd_timestamps[i]:
                missing_timestamps.append("(%s -- %s)" % (pd_timestamps[i-1], pd_timestamps[i]))
            i += 1
        for v in missing_timestamps:
            print(v)
        assert len(missing_timestamps) == 0

    def get_matrix(self, timestamp):
        return self.data[self.get_index[timestamp]]

    def save(self, fname):
        pass

    def check_it(self, depends):  # 判断是否有符合条件的一天
        for d in depends:
            if d not in self.get_index.keys():  #返回一个字典所有的键
                return False
        return True

    #用于生成用于训练的数据
    def create_dataset(self, len_closeness=3, len_trend=3, TrendInterval=7, len_period=3, PeriodInterval=1):
        # 趋势间隔7
        # 周期间隔1
        # 近期，周期，趋势长度均为3
        """current version
        """
        # offset_week = pd.DateOffset(days=7)
        offset_frame = pd.DateOffset(minutes=24 * 60 // self.T) # 日期偏移 每次时间偏移30分钟
        XC = []  # 近期训练集合（num, 6, 32, 32)
        XP = []  # 周期训练集合（num, 2, 32, 32)
        XT = []  # 趋势训练集合 (num, 2, 32, 32)
        Y = []   # 目标集合 (num, 2, 32, 32)
        timestamps_Y = []  #日期集合
        # 时间依赖
        # # 输出结果：[range(1, 4), [48], [336]]
        # 近期：1，2，3
        # 周期：48
        # 趋势：336
        # #
        depends = [range(1, len_closeness+1),
                   [PeriodInterval * self.T * j for j in range(1, len_period+1)],
                   [TrendInterval * self.T * j for j in range(1, len_trend+1)]]

        i = max(self.T * TrendInterval * len_trend, self.T * PeriodInterval * len_period, len_closeness) # i =336
        while i < len(self.pd_timestamps):
            Flag = True
            for depend in depends:  # depends=[1, 2, 3, 48, 336]
                if Flag is False:
                    # print("test", self.pd_timestamps[i])
                    break
                Flag = self.check_it([self.pd_timestamps[i] - j * offset_frame for j in depend])
                #用于训练的数据必须满足近期(连续3个时段)，周期（间隔48个时段，一天），趋势数据（间隔7*48个时段，一周）
                #近期：[<DateOffset: kwds={'minutes': 30}>, <2 * DateOffsets: kwds={'minutes': 30}>, <3 * DateOffsets: kwds={'minutes': 30}>]
                #周期：[<48 * DateOffsets: kwds={'minutes': 30}>]
                #趋势：[<336 * DateOffsets: kwds={'minutes': 30}>]

            if Flag is False:
                i += 1
                continue
            #合并格式
            x_c = [self.get_matrix(self.pd_timestamps[i] - j * offset_frame) for j in depends[0]] #3个时间段的通道数据
            x_p = [self.get_matrix(self.pd_timestamps[i] - j * offset_frame) for j in depends[1]] #1个时间段的通道数据
            x_t = [self.get_matrix(self.pd_timestamps[i] - j * offset_frame) for j in depends[2]] #1个时间段的通道数据
            y = self.get_matrix(self.pd_timestamps[i]) #保存目标节点的数据

            if len_closeness > 0:
                XC.append(np.vstack(x_c)) # 近期训练数据（6, 32, 32)
            if len_period > 0:
                XP.append(np.vstack(x_p)) # 周期训练数据（2, 32, 32)
            if len_trend > 0:
                XT.append(np.vstack(x_t)) # 趋势训练数据（2, 32, 32)
            Y.append(y)  # （2, 32, 32)
            timestamps_Y.append(self.timestamps[i])
            i += 1
        XC = np.asarray(XC)
        XP = np.asarray(XP)
        XT = np.asarray(XT)
        Y = np.asarray(Y)
        print("XC shape: ", XC.shape, "XP shape: ", XP.shape, "XT shape: ", XT.shape, "Y shape:", Y.shape)
        print("timestamp_Y: ",timestamps_Y)
        return XC, XP, XT, Y, timestamps_Y


if __name__ == '__main__':
    pass
