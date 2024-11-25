'''
新舊模型比較(片長節省率)
'''
import csv
import cv2
import os
from datetime import datetime

def calc_video_length_saving_rate(total_video_frame: int, total_event_frame: int) -> float:
    """計算片長節省率。

    Args:
        total_video_frame (int): 總共的輸入影片幀數。
        total_event_frame (int): 判讀結果的事件總幀數。

    Returns:
        float: 百分比，四捨五入制小數點第2位。
    """
    return round((total_video_frame - total_event_frame) / total_video_frame * 100, 2)

def create_initial_dict(model_dict: dict) -> dict:
    """創建初始化的統計字典。

    Args:
        model_dict (dict): 要統計的模型列表。

    Returns:
        dict: 回傳的統計字典。
    """
    info_dict = {}
    for version, model_name in model_dict.items():
        single_model_dict = {model_name: {'total_event_count': 0, 'total_video_frame': 0, 'total_event_frame': 0}}
        info_dict = {**info_dict, **single_model_dict}
    return info_dict

def find_model_version(model_dict: dict, model_name: str) -> str:
    """傳入model name，回傳對應的version。

    Args:
        model_dict (dict): 模型字典。
        model_name (str): 要找version的模型名稱。

    Returns:
        str: version.
    """
    for version, name in model_dict.items():
        if model_name == name:
            return version
    return None

def date_formatter(date: str) -> str:
    # 使用 datetime.strptime 解析日期字符串
    parsed_date = datetime.strptime(date, '%Y-%m-%d')
    # 使用 datetime.strftime 格式化日期为所需格式
    formatted_date = parsed_date.strftime('%Y%m%d')
    return formatted_date

def calc_event_frame(file_path: str) -> int:
    total = 0
    with open(file_path, newline='') as f:
        rows = csv.reader(f)
        for row in rows:
            total += (int(row[1]) - int(row[0])) + 1
    return total

def calc_video_frame(file_path: str) -> int:
    cap = cv2.VideoCapture(file_path)
    frames_num_of_input_video = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    return frames_num_of_input_video


if __name__ == '__main__':
    csv_file_dict = {('v1', 'water'): '/home/ryan/nas/nas_ryan/EPA-Dissipation/code/video_process_info_v1_water.csv',
                     ('v1', 'other'): '/home/ryan/nas/nas_ryan/EPA-Dissipation/code/video_process_info_v1_other.csv',
                     ('v4', 'water'): '/home/ryan/nas/nas_ryan/EPA-Dissipation/code/video_process_info_v4_water.csv',
                     ('v4', 'other'): '/home/ryan/nas/nas_ryan/EPA-Dissipation/code/video_process_info_v4_other.csv',
                     ('v75', 'water'): '/home/ryan/nas/nas_ryan/EPA-Dissipation/code/video_process_info_v75_water.csv',
                     ('v75', 'other'): '/home/ryan/nas/nas_ryan/EPA-Dissipation/code/video_process_info_v75_other.csv',
                     ('v825', 'water'): '/home/ryan/nas/nas_ryan/EPA-Dissipation/code/video_process_info_v825_water.csv',
                     ('v825', 'other'): '/home/ryan/nas/nas_ryan/EPA-Dissipation/code/video_process_info_v825_other.csv',
                     ('v827', 'water'): '/home/ryan/nas/nas_ryan/EPA-Dissipation/code/video_process_info_v827_water.csv',
                     ('v827', 'other'): '/home/ryan/nas/nas_ryan/EPA-Dissipation/code/video_process_info_v827_other.csv'}

    model_dict = {'v1': 'acc_91_p254_n806_feature_20',
                  'v4': 'acc_97_p3461_n3461_feature_21',
                  'v75': 'acc_97_p3585_n3585_feature_21',
                  'v825': 'acc_93_p1273_n3585_feature_21',
                  'v827': 'acc_94_p1321_n3585_feature_21'}
    
    result_path_dict = {('v1', 'water'): '/home/ryan/nas/nas_ryan/EPA-Dissipation/result_0829_test_v1_model_water',
                        ('v1', 'other'): '/home/ryan/nas/nas_ryan/EPA-Dissipation/result_0830_test_v1_model_other',
                        ('v4', 'water'): '/home/ryan/nas/nas_ryan/EPA-Dissipation/result_0906_test_v4_model_water',
                        ('v4', 'other'): '/home/ryan/nas/nas_ryan/EPA-Dissipation/result_0908_test_v4_model_other',
                        ('v75', 'water'): '/home/ryan/nas/nas_ryan/EPA-Dissipation/result_1007_test_v75_model_water',
                        ('v75', 'other'): '/home/ryan/nas/nas_ryan/EPA-Dissipation/result_1009_test_v75_model_other',
                        ('v825', 'water'): '/home/ryan/nas/nas_ryan/EPA-Dissipation/result_1104_test_v825_model_water',
                        ('v825', 'other'): '/home/ryan/nas/nas_ryan/EPA-Dissipation/result_1106_test_v825_model_other',
                        ('v827', 'water'): '/home/ryan/nas/nas_ryan/EPA-Dissipation/result_1108_test_v827_model_water',
                        ('v827', 'other'): '/home/ryan/nas/nas_ryan/EPA-Dissipation/result_1110_test_v827_model_other'}

    statistic_dict = create_initial_dict(model_dict)

    for case, file_path in csv_file_dict.items():
        with open(file_path, encoding='utf-8-sig', newline='') as csvfile:
            rows = csv.DictReader(csvfile)
            for row in rows:
                statistic_dict[row['model']]['total_event_count'] += int(row['event_cnt']) # 統計總事件數

                result_path = result_path_dict[case] # 取得結果路徑

                csv_path = os.path.join(result_path, row['factory'], row['date'], row['time'], row['camera_ID'], 'csv', date_formatter(row['date'])+'-'+row['time']+'.csv')
                video_path = os.path.join(result_path, row['factory'], row['date'], row['time'], row['camera_ID'], 'final', date_formatter(row['date'])+'-'+row['time']+'.mp4')

                total_event_frame = calc_event_frame(csv_path)
                total_video_frame = calc_video_frame(video_path)

                statistic_dict[row['model']]['total_event_frame'] += total_event_frame
                statistic_dict[row['model']]['total_video_frame'] += total_video_frame

    # print(statistic_dict)
    for model, info in statistic_dict.items():
        print(model)
        for k, v in info.items():
            print(f'    {k}: {v}')

    for model, info in statistic_dict.items():
        rate = calc_video_length_saving_rate(total_event_frame=info['total_event_frame'], total_video_frame=info['total_video_frame'])
        version = find_model_version(model_dict, model)
        print(f'{version} saving rate: {rate}%')