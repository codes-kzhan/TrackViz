# coding=utf-8
from serialize import pickle_load


def binary_search(a, target):
    # 不同于普通的二分查找，目标是寻找target最适合的index
    low = 0
    high = len(a) - 1

    while low <= high:
        # 在其它语言中,如果low + high的和大于Integer的最大值,比如2 ** 31 - 1,
        # 计算便会发生溢出,使它成为一个负数,然后被2除时结果仍为负数。在Java语言中,
        # 这个Bug导致一个ArrayIndexOutOfBoundsException异常被抛出,而在C语言中,
        # 你会得到一个无法预测的越界的数组下标。推荐的解决方法是修改中间值的计算过程,
        # 方法之一是用减法而不是加法——来实现：mid = low + ((high - low) / 2)；或者,
        # 如果你想炫耀一下自己掌握的移位运算的知识,可以使用更快的移位运算操作,
        # 在Python中是mid = (low + high) >> 1,Java中是int mid = (low + high) >>> 1。
        mid = (low + high) // 2
        midVal = a[mid]

        if midVal < target:
            low = mid + 1
        elif midVal > target:
            high = mid - 1
        else:
            return mid
    return low


def track_score(camera1, time1, camera2, time2):
    camera1 -= 1
    camera2 -= 1
    camera_delta_s = pickle_load('top10/sorted_deltas.pickle')
    cur_delta = time2 - time1
    delta_distribution = camera_delta_s[camera1][camera2]
    # 30 second
    interval = 1 * 30 * 25
    left_bound = cur_delta - interval
    right_bound = cur_delta + interval
    left_index = binary_search(delta_distribution, left_bound)
    right_index = binary_search(delta_distribution, right_bound)
    print(len(delta_distribution))
    print('delta range %d - %d' % (delta_distribution[0], delta_distribution[-1]))
    print(left_index)
    print(right_index)
    print('probablity: %f%%' % ((right_index - left_index) / float(len(delta_distribution)) * 100))

if __name__ == '__main__':
    track_score(1, 500, 3, 0)