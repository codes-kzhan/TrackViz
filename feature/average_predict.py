import random
import shutil

from feature.top10distribution import get_tracks, get_predict_tracks, store_sorted_deltas
from profile.fusion_param import get_fusion_param, ctrl_msg
from util.file_helper import write, safe_mkdir, safe_remove
from util.str_helper import folder


def write_rand_pid():
    fusion_param = get_fusion_param()
    rand_answer_path = fusion_param['answer_path'].replace(ctrl_msg['data_folder_path'], ctrl_msg['data_folder_path'] + '_rand')
    rand_folder_path = folder(rand_answer_path)
    safe_mkdir(rand_folder_path)
    shutil.copy(fusion_param['answer_path'], rand_answer_path)
    rand_path = rand_folder_path + '/renew_pid.log'
    safe_remove(rand_path)

    origin_tracks = get_tracks()
    origin_pids = [track.split('_')[0] for track in origin_tracks]
    pid_cnt = len(origin_pids)
    persons_rand_predict_idx_s = [random.sample(origin_pids, pid_cnt) for _ in range(pid_cnt)]
    write_content = ''
    for rand_predict_idx_s in persons_rand_predict_idx_s:
        for rand_predict_idx in rand_predict_idx_s:
            write_content += rand_predict_idx + ' '
        write_content += '\n'
    write(rand_path, write_content)


def gen_rand_st_model():
    ctrl_msg['data_folder_path'] = ctrl_msg['data_folder_path'] + '_rand'
    get_predict_tracks()
    # get distribution sorted list for probability compute
    store_sorted_deltas()

if __name__ == '__main__':
    write_rand_pid()
    gen_rand_st_model()