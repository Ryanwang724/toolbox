import csv
import cv2
import os
from datetime import datetime
from typing import List, Tuple, Union


class VideoClipper:
    def __init__(self, input_csv_file: str, input_video_path: str, output_video_path: str, fps: int, window_length: int, front_buffer_frames: int, back_buffer_frames: int, max_event: int):
        self.input_csv_file = input_csv_file
        self.input_video_path = input_video_path
        self.output_video_path = output_video_path
        os.makedirs(output_video_path, exist_ok=True)
        self.fps = fps
        self.window_length = window_length
        self.front_buffer_frames = front_buffer_frames
        self.back_buffer_frames = back_buffer_frames
        self.max_event = max_event

    def __video_name_merge(self, row: dict) -> str:
        formatted_date = datetime.strptime(row['日期'], '%Y/%m/%d').strftime('%Y%m%d')
        formatted_time = datetime.strptime(row['時間'], "%H:%M:%S").strftime("%H%M%S")
        file_name = [row['受補貼機構'], row['鏡頭編號'], formatted_date, formatted_time + '.mp4']
        file_name = '-'.join(file_name)

        return file_name
    
    def __calc_video_total_frame(self, file_name: str) -> int:
        video_path = os.path.join(self.input_video_path, file_name)
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise FileNotFoundError(f'Cannot open video file: {video_path}')
        
        video_total_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.release()

        return video_total_frame

    def __calc_frame(self, event_timestamps: str, video_total_frame: int) -> List[Tuple[int, int]]:
        event_timestamps = event_timestamps.split(',')
        result_list = []
        for timestamp in event_timestamps:
            time_obj = datetime.strptime(timestamp, "%H:%M:%S")
            total_seconds = time_obj.minute * 60 + time_obj.second # 只考慮分鐘和秒數，忽略小時
            # print(total_seconds)

            # 計算前後緩衝長度
            front_buffer = self.window_length + self.front_buffer_frames
            back_buffer = self.back_buffer_frames
            target_frame = total_seconds * self.fps

            # 前後緩衝長度修正(boundary condition)
            start_frame = max(0, target_frame - front_buffer)
            end_frame = min(video_total_frame, target_frame + back_buffer)

            # print((int(start_frame), int(end_frame)))
            result_list.append((int(start_frame), int(end_frame)))
        
        # # 合併相近範圍 NOTE: 不合併可能比較好，可以跳過中間的累積背景模型部分
        # merged_result = []
        # current_start, current_end = result_list[0]

        # for next_start, next_end in result_list[1:]:
        #     # 如果後一個事件的起始幀小於或等於前一個事件的結束幀，則合併
        #     if next_start <= current_end:
        #         current_end = max(current_end, next_end)  # 擴展結束幀
        #     else:
        #         merged_result.append((current_start, current_end))
        #         current_start, current_end = next_start, next_end

        # # 最後一個範圍
        # merged_result.append((current_start, current_end))

        # return merged_result
        return result_list

    def __clip(self, file_name: str, event_list: List[Tuple[int, int]]):
        video_path = os.path.join(self.input_video_path, file_name)
        cap = cv2.VideoCapture(video_path)
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        codec = cv2.VideoWriter_fourcc(*'mp4v')

        for index, (start_frame, end_frame) in enumerate(event_list, start=1):
            if len(event_list) > 1:
                output_file_name = f"{os.path.splitext(file_name)[0]}_{index}.mp4"
            else:
                output_file_name = file_name

            split_file_name = file_name.split('-')
            split_file_name[-1], file_extension = split_file_name[-1].split('.')

            output_video_dir = split_file_name[0] + '-' + split_file_name[1]
            time_dir = split_file_name[2] + '-' + split_file_name[3]
            os.makedirs(os.path.join(self.output_video_path, output_video_dir, time_dir), exist_ok=True)
            output_file_path = os.path.join(self.output_video_path, output_video_dir, time_dir, output_file_name)

            out = cv2.VideoWriter(output_file_path, codec, self.fps, (frame_width, frame_height))
            cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
            for frame_num in range(start_frame, end_frame + 1):
                ret, frame = cap.read()
                if not ret:
                    print(f"Warning: Reached end of video before frame {end_frame}.")
                    break

                out.write(frame)
            out.release()
        cap.release()

    def execute(self, start: Union[int, None]):
        with open(self.input_csv_file, 'r', newline='', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)

            for index, row in enumerate(reader, start=2): # 設為從2開始，方便和csv對照
                if start is not None:
                    if index < start:
                        continue
                if row['項目'] == '冷煤' and len(row['異常時間點'].split(',')) < self.max_event:
                    file_name = self.__video_name_merge(row)
                    print(f'Now Processing... {index}: {file_name}')
                    video_total_frame = self.__calc_video_total_frame(file_name=file_name)
                    events_time_list = self.__calc_frame(row['異常時間點'], video_total_frame)
                    self.__clip(file_name, events_time_list)

                    if index == 3: # 測試用，只測前幾項就停
                        break

                else: # 直接跳過大門case
                    continue

if __name__ == '__main__':
    INPUT_CSV_FILE = '202305~202309 異常事件.csv'
    INPUT_VIDEO_PATH = os.path.join('.', 'input')    # 輸入影片路徑
    OUTPUT_VIDEO_PATH = os.path.join('.', 'output')  # 輸出影片路徑
    FPS = 6.99
    WINDOW_LENGTH = 300
    FRONT_BUFFER_FRAMES = 35 # 噴發時間點的前方緩衝幀數
    BACK_BUFFER_FRAMES = 35  # 噴發時間點的後方緩衝幀數
    MAX_EVENT = 10           # 該時段最大事件數，超過通常是有異常，就跳過不處理
    START = None             # 設定要從第幾項開始跑，預設為None


    video_clipper = VideoClipper(input_csv_file=INPUT_CSV_FILE,
                                 input_video_path=INPUT_VIDEO_PATH,
                                 output_video_path=OUTPUT_VIDEO_PATH,
                                 fps=FPS,
                                 window_length=WINDOW_LENGTH,
                                 front_buffer_frames=FRONT_BUFFER_FRAMES,
                                 back_buffer_frames=BACK_BUFFER_FRAMES,
                                 max_event=MAX_EVENT)
    video_clipper.execute(start=START)