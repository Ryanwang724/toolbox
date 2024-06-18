import cv2
import csv
import os
import re


class PlayEventVideo:
    """確認冷媒噴發時間點"""
    FPS = 6.993
    SEC = 5
    def __init__(self, csv_input_path:str, video_input_path:str, file_info_dict:dict):
        self.csv_input_path = csv_input_path
        self.video_input_path = video_input_path
        self.file_info_dict = file_info_dict

        self.buffer_length = int(self.SEC * self.FPS)

        self.file_name = self.file_info_dict['factory_name'] + '-' + self.file_info_dict['camera_id'] + '-' + re.split(r'/|\.', self.csv_input_path)[-2] + '_checked.csv'

    def _read_csv_data(self):
        if os.path.isfile(self.csv_input_path):
            with open(self.csv_input_path) as csvFile:
                csvReader = csv.reader(csvFile)
                self.event_list = list(csvReader)

            print(f'Total Event Count: {len(self.event_list)}')
        else:
            print('invalid csv_input_path')
            return
    
    def _check_input_video(self):
        if not os.path.isfile(self.video_input_path):
            print('invalid video_input_path')
            return

    def execute(self):
        self._read_csv_data()
        self._check_input_video()

        process_name = file_info_dict['factory_name'] + '-' + file_info_dict['camera_id']+ '-' + file_info_dict['date']+ '-' + file_info_dict['time']
        
        time_min_bias = int(file_info_dict['time'][2:4])
        time_sec_bias = int(file_info_dict['time'][4:])

        cap = cv2.VideoCapture(self.video_input_path)
        print("frame rate = ",cap.get(cv2.CAP_PROP_FPS))
        total_frame = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        print("Video total frame = ",total_frame)

        if not self.event_list:
            print(f'No events to process. {process_name}')
            return
        
        frame_count = 0
        for i in range(0, len(self.event_list)-2):  # 最後兩欄為統計
            event  = self.event_list[i]
            if int(event[2]) == 1: # 複判是冷媒才做後續
                event[0] = int(event[0]) # str to int
                event[1] = int(event[1])

                if event[0] < self.buffer_length:  # check boundary condition
                    start_frame = 0
                else:
                    start_frame = event[0] - self.buffer_length
                if event[1] > total_frame - self.buffer_length:
                    end_frame = total_frame
                else:
                    end_frame = event[1] + self.buffer_length
            
                while True:
                    cap.set(cv2.CAP_PROP_POS_FRAMES,start_frame)
                    frame_count = start_frame
                    while frame_count < end_frame:
                        ret, frame = cap.read()
                        if not ret:
                            break
                        cv2.imshow('frame', frame)
                        frame_count += 1
                        if cv2.waitKey(30) == ord('q'):
                            cap.release()
                            cv2.destroyAllWindows()
                            return
                    hint_start_time = divmod(int(event[0]/self.FPS), 60)
                    hint_end_time = divmod(int(event[1]/self.FPS), 60)
                    duration = (int(event[1]) - int(event[0])) / self.FPS
                    print(f'This event [{i}/{len(self.event_list)}] frame:{event[0]} ~ {event[1]} '
                        f'({(hint_start_time[0]+time_min_bias):02}:{(hint_start_time[1]+time_sec_bias):02} ~ '
                        f'{(hint_end_time[0]+time_min_bias):02}:{(hint_end_time[1]+time_sec_bias):02}, {duration:.2f} sec) '
                        'is Refrigerant? (y:yes  n:no  q:exit  other:replay)')
                    user_input_key = cv2.waitKey(0)   
                    if user_input_key == ord('y'):
                        print(f'This event [{i}/{len(self.event_list)-2}] is \x1b[6;30;42m' + 'yes' + '\x1b[0m'+', play next.')
                        break
                    elif user_input_key == ord('n'):
                        print(f'This event [{i}/{len(self.event_list)-2}] is \x1b[6;30;41m' + 'no' + '\x1b[0m'+', play next.')
                        break
                    elif user_input_key == ord('q'):
                        cap.release()
                        cv2.destroyAllWindows()
                        return

        print('All events are checked!')

        cap.release()
        cv2.destroyAllWindows()
        
        print(f'[PlayEventVideo] "{process_name}" done.')



if __name__ == '__main__':
# ================================================
    filename = '20240410-160000'
    factory_name = '弘光'
    camera_id = '5071927718'
# ================================================
    date, time = filename.split('-')
    date = date[:4] + '-' + date[4:6] + '-' + date[6:]

    file_info_dict = dict()
    file_info_dict['factory_name'] = factory_name
    file_info_dict['date'] = date
    file_info_dict['time'] = time
    file_info_dict['camera_id'] = camera_id

    current_dir = os.path.dirname(os.path.abspath(__file__))
# ================================================
    result_path = os.path.join(current_dir, '..', 'EPA-Dissipation', 'result_0514_rerun')
    middle_path = os.path.join(factory_name, date, time, camera_id)
    checked_filename = factory_name + '-' + camera_id + '-' + filename + '_checked.csv'
    csv_input_path = os.path.join(current_dir, 'input', checked_filename)
    video_path = os.path.join(result_path, middle_path, 'final', filename + '.mp4')
# ================================================
    
    play_event_video = PlayEventVideo(csv_input_path = csv_input_path,     # 選擇需要的路徑
                                      video_input_path = video_path,       # 選擇需要的路徑
                                      file_info_dict = file_info_dict)
    play_event_video.execute()

