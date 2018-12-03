'''
数据信息描述
1. *.h5数据大小
2. 涉及天数，开始时间—结束时间
3. 应有时间间隙
4. 可用的时间间隙
5. 时间间隙丢失率
6. 人流量最大，最小值
'''
from __future__ import print_function
import h5py
import time

def load_stdata(fname):
    f = h5py.File(fname, 'r')
    data = f['data'].value
    timestamps = f['date'].value
    f.close()
    return data, timestamps


def stat(fname): #查看数据状态
    def get_nb_timeslot(f):
        start_time = f['date'][0]   #获取数据第一条的日期 eg: 2013070101
        end_time = f['date'][-1]  #获取数据最后一条的日期 eg: 2013102948
        # 使用切片获取开始时间的 年，月，日
        year, month, day = map(int, [start_time[:4], start_time[4:6], start_time[6:8]])
        ts = time.strptime("%04i-%02i-%02i" % (year, month, day), "%Y-%m-%d")
        # 使用切片获取结束时间的 年，月，日
        year, month, day = map(int, [end_time[:4], end_time[4:6], end_time[6:8]])
        te = time.strptime("%04i-%02i-%02i" % (year, month, day), "%Y-%m-%d")
        nb_day = (time.mktime(te) - time.mktime(ts)) / (86400) + 1
        nb_timeslot = nb_day * 48
        ts_str, te_str = time.strftime("%Y-%m-%d", ts), time.strftime("%Y-%m-%d", te)
        return nb_day, nb_timeslot, ts_str, te_str

    with h5py.File(fname) as f:
        nb_day, nb_timeslot, ts_str, te_str = get_nb_timeslot(f)
        mmax = f['data'].value.max()  # 获取流入流出的最大值
        mmin = f['data'].value.min()  # 获取流入流出的最小值
        stat = '=' * 5 + 'stat' + '=' * 5 + '\n' + \
               'filename: %s\n' % (fname)+\
               'data shape: %s\n' % str(f['data'].shape) + \
               '# of days: %i, from %s to %s\n' % (nb_day, ts_str, te_str) + \
               '# of timeslots: %i\n' % int(nb_timeslot) + \
               '# of timeslots (available): %i\n' % f['date'].shape[0] + \
               'missing ratio of timeslots: %.1f%%\n' % ((1. - float(f['date'].shape[0] / nb_timeslot)) * 100) + \
               'max: %.3f, min: %.3f\n' % (mmax, mmin) + \
               '=' * 5 + 'stat' + '=' * 5 + '\n'
        print(stat)
#
# ##测试代码：
# stat('BJ13_M32x32_T30_InOut.h5')
# stat('BJ14_M32x32_T30_InOut.h5')
# stat('BJ15_M32x32_T30_InOut.h5')
# stat('BJ16_M32x32_T30_InOut.h5')