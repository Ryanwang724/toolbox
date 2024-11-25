import csv
from collections import defaultdict


def statistic_result(video_model_stats: dict, csv_files: list) -> dict:
    for csv_file in csv_files:
        with open(csv_file, mode='r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            # 累計每個factory, camera_ID和channel的模型事件數和run_time
            for row in reader:
                try:
                    factory = row['factory']
                    camera_id = row['camera_ID']
                    channel = row['channel']
                    model = row['model']
                    event_count = int(row['event_cnt'])
                    run_time = float(row['run_time'])
                    video_key = (factory, camera_id, channel)
                    video_model_stats[video_key][model]['event_count'] += event_count
                    video_model_stats[video_key][model]['total_run_time'] += run_time
                except KeyError as e:
                    print(f"Missing key in row: {row}, error: {e}")
                except ValueError as e:
                    print(f"Value error in row: {row}, error: {e}")
    return video_model_stats

# 顯示結果
def show_video_model_stat(video_model_stats: dict):
    for video_key, model_stats in video_model_stats.items():
        factory, camera_id, channel = video_key
        print(f'Factory: {factory}, Camera ID: {camera_id}, Channel: {channel}')
        for model, stats in model_stats.items():
            event_count = stats['event_count']
            total_run_time = stats['total_run_time']
            print(f'    Model: {model}, Total Event Count: {event_count}, Total Run Time: {total_run_time:.3f} seconds')

# 將結果寫入新的CSV文件
def write_result(output_file: str, video_model_stats: dict):
    with open(output_file, mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow(['Factory', 'Camera ID', 'Channel', 'Model', 'Total Event Count', 'Total Run Time'])
        
        for video_key, model_stats in video_model_stats.items():
            factory, camera_id, channel = video_key
            for model, stats in model_stats.items():
                event_count = stats['event_count']
                total_run_time = stats['total_run_time']
                writer.writerow([factory, camera_id, channel, model, event_count, total_run_time])

    print(f'Results saved to {output_file}')

if __name__ == '__main__':
    # 初始化嵌套字典來存儲factory, camera_ID和channel的模型事件數和run_time
    video_model_stats = defaultdict(lambda: defaultdict(lambda: {'event_count': 0, 'total_run_time': 0.0}))

    # 讀取CSV文件
    # NOTE: 這是使用各channel事件相加，因此實際事件應該會比這個少
    csv_files = ['/home/ryan/nas/nas_ryan/EPA-Dissipation/code/video_process_info_v1_other.csv',
                 '/home/ryan/nas/nas_ryan/EPA-Dissipation/code/video_process_info_v1_water.csv',
                 '/home/ryan/nas/nas_ryan/EPA-Dissipation/code/video_process_info_v75_water.csv',
                 '/home/ryan/nas/nas_ryan/EPA-Dissipation/code/video_process_info_v75_other.csv',
                 '/home/ryan/nas/nas_ryan/EPA-Dissipation/code/video_process_info_v825_other.csv',
                 '/home/ryan/nas/nas_ryan/EPA-Dissipation/code/video_process_info_v825_water.csv',
                 '/home/ryan/nas/nas_ryan/EPA-Dissipation/code/video_process_info_v827_other.csv',
                 '/home/ryan/nas/nas_ryan/EPA-Dissipation/code/video_process_info_v827_water.csv']  # 放入要被放至同張表比較的csv
    
    video_model_stats = statistic_result(video_model_stats, csv_files)
    show_video_model_stat(video_model_stats)
    OUTPUT_FILE_NAME = 'result.csv'
    write_result(OUTPUT_FILE_NAME, video_model_stats)