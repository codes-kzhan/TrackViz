#coding=utf-8
from random import randint

from util.file_helper import read_lines, safe_remove
from util.serialize import pickle_save


def get_predict_delta_tracks(fusion_param, useful_predict_cnt=10, random=False):
    # 获取左图列表
    answer_path = fusion_param['answer_path']
    answer_lines = read_lines(answer_path)

    real_tracks = list()
    for answer in answer_lines:
        info = answer.split('_')
        if 'bmp' in info[2]:
            #
            info[2] = info[2].split('.')[0]
        if len(info) > 4 and 'jpe' in info[6]:
            # grid
            real_tracks.append([info[0], int(info[1][0]), int(info[2]), 1])
        else:
            # market
            real_tracks.append([info[0], int(info[1][1]), int(info[2]), int(info[1][3])])
    print 'left image ready'
    # 获取右图列表
    renew_pid_path = fusion_param['renew_pid_path']
    predict_lines = read_lines(renew_pid_path)
    print 'predict images ready'
    camera_cnt = 6
    # 左图中的人在右图可能出现在6个摄像头中
    camera_delta_s = [[list() for j in range(camera_cnt)] for i in range(camera_cnt)]
    person_cnt = len(answer_lines)
    # market1501数据集有六个序列，只有同一个序列才能计算delta
    for i, line in enumerate(predict_lines):
        predict_pids = line.split(' ')
        for j, predict_pid in enumerate(predict_pids):
            if j > useful_predict_cnt:
                break
            if random:
                predict_pid = randint(0, person_cnt)
            else:
                predict_pid = int(predict_pid) - 1
            # same seq
            if real_tracks[i][3] == real_tracks[predict_pid][3]:
                delta = real_tracks[i][2] - real_tracks[predict_pid][2]
                if abs(delta) < 1000000:
                    camera_delta_s[real_tracks[i][1] - 1][real_tracks[predict_pid][1] - 1].append(delta)
    print 'deltas collected'
    for camera_delta in camera_delta_s:
        for delta_s in camera_delta:
            delta_s.sort()
    print 'deltas sorted'
    # for python
    if random:
        safe_remove(fusion_param['distribution_pickle_path'])
        pickle_save(fusion_param['distribution_pickle_path'], camera_delta_s)
        print 'deltas saved'
    else:
        print 'not random, nothing saved'
    return camera_delta_s