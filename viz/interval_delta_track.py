import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from pre_process.raw_data import camera_cnt
from profile.fusion_param import get_fusion_param
from util.file_helper import read_lines_and

data_type = 0
viz_local = True


def camera_intervals(fusion_param, camera_num):
    # fusion_param = get_fusion_param()
    intervals = list()
    cur_values = {'id': 0, 'start': 0, 'end': 0}

    def count_interval(img_name):
        if '.' not in img_name:
            return
        track_info = img_name.split('.')[0].split('_')
        person_id = track_info[0]
        track_time = int(track_info[2])
        if person_id != cur_values['id']:
            intervals.append([cur_values['id'], cur_values['start'], cur_values['end']])
            cur_values['id'] = person_id
            cur_values['start'] = track_time
            cur_values['end'] = track_time
        else:
            if track_time > cur_values['end']:
                cur_values['end'] = track_time
    if data_type == 0:
        # read_lines_and('market_s1/track_c%ds1.txt' % (camera_num), count_interval)
        read_lines_and(fusion_param['predict_camera_path'] + camera_num + '.txt', count_interval)
    else:
        read_lines_and(fusion_param['predict_camera_path'] + camera_num + '.txt', count_interval)
    return intervals[1:]


def find_id_delta(intervals, id, frame):
    frame = int(frame)
    for interval in intervals:
        if interval[0] == id:
            delta0 = frame - interval[1]
            delta1 = frame - interval[2]
            if abs(delta0) < abs(delta1):
                return delta0
            else:
                return delta1
        else:
            continue
    return -0.1


def camera_distribute(camera_num):
    fusion_param = get_fusion_param()
    intervals = camera_intervals(fusion_param, camera_num)
    print('get intervals for c%d' % camera_num)
    deltas = [list() for i in range(6)]
    cur_delta = {'id': 0, 'delta': 1000000, 'camera': -1}

    def shuffle_person(img_name):
        if '.' not in img_name:
            return
        track_info = img_name.split('.')[0].split('_')
        person_id = track_info[0]
        track_delta = find_id_delta(intervals, person_id, int(track_info[2]))
        camera_id = int(track_info[1][1])
        if track_delta == -0.1:
            # id not found
            cur_delta['id'] = 0
            return
        # new id, has appeared in camera -camera_num
        cur_delta['id'] = person_id
        cur_delta['delta'] = track_delta
        cur_delta['camera'] = camera_id

        if cur_delta['id'] != 0:
            # exclude first zero record and not found id records
            # deltas.append([cur_delta['id'], cur_delta['camera'], cur_delta['delta']])
            # ignore large data
            if abs(cur_delta['delta']) < 2000:
                deltas[cur_delta['camera'] - 1].append(cur_delta['delta'])
    if data_type == 0:
        # read_lines_and('market_s1/track_s1.txt', shuffle_person)
        read_lines_and(fusion_param['predict_track_path'], shuffle_person)
    else:
        read_lines_and(fusion_param['predict_track_path'], shuffle_person)
    return deltas


def viz_data_for_market():
    track_distribute = list()
    for i in range(camera_cnt):
        track_distribute.append(camera_distribute(i + 1))
    return track_distribute


def distribute_in_cameras(data_s, subplot, camera_id):
    sns.set(color_codes=True)
    for i, data in enumerate(data_s):
        sns.distplot(np.array(data), label='camera %d' % (i + 1), hist=False, ax=subplot, axlabel='Distribution for camera %d' % camera_id)


def viz_market_distribution():
    viz_data = viz_data_for_market()
    f, axes = plt.subplots(3, 2, figsize=(15, 10))
    if viz_local:
        for ax_s in axes:
            for ax in ax_s:
                ax.set_xlabel('time')
                ax.set_ylabel('appear density')
                # ax.set_xlim([-2000, 2000])
                # ax.set_ylim([0, 0.025])
    sns.despine(left=True)
    for i in range(camera_cnt):
        # sns.plt.title('Appear distribution in cameras %d' % (i + 1))
        distribute_in_cameras(viz_data[i], axes[i / 2, i % 2], i + 1)
        print('viz camera %d' % (i + 1))
    sns.plt.show()


def deltas2track():
    viz_data = viz_data_for_market()
    track = [[list(), list()] for _ in range(6)]
    for i, camera_deltas in enumerate(viz_data):
        for j, per_camera_deltas in enumerate(camera_deltas):
            for delta in per_camera_deltas:
                track[i][0].append(j + 1)
                track[i][1].append(delta)
    return track


def distribute_joint(data_s, subplot, camera_id):
    sns.kdeplot(np.array(data_s[0]), np.array(data_s[1]), shade=True, bw="silverman", ax=subplot, cmap="Purples")
    # subplot.scatter(data_s[0], data_s[1], s=10, c='g', marker='o')


def viz_market():
    viz_data = deltas2track()
    f, axes = plt.subplots(3, 2)
    if viz_local:
        for i, ax_s in enumerate(axes):
            for j, ax in enumerate(ax_s):
                ax.set_title('Distribution for camera %d' % (i * 2 + j))
                # ax.set_xlabel('camera')
                ax.set_ylabel('time')
                ax.set_ylim([-3000, 3000])
    sns.despine(left=True)
    for i in range(camera_cnt):
        # sns.plt.title('Appear distribution in cameras %d' % (i + 1))
        distribute_joint(viz_data[i], axes[i / 2, i % 2], i + 1)
        print('viz camera %d' % (i + 1))
    sns.plt.show()


if __name__ == '__main__':
    # print(camera_distribute(1))
    viz_market_distribution()
    # viz_market()