import csv
import os
import requests
from datetime import datetime


class VideoDownloader:
    def __init__(self, input_csv_file: str, output_dir: str):
        self.input_csv_file = input_csv_file
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def __video_name_merge(self, row: dict) -> str:
        formatted_date = datetime.strptime(row['日期'], '%Y/%m/%d').strftime('%Y%m%d')
        formatted_time = datetime.strptime(row['時間'], "%H:%M:%S").strftime("%H%M%S")
        file_name = [row['受補貼機構'], row['鏡頭編號'], formatted_date, formatted_time + '.mp4']
        file_name = '-'.join(file_name)

        return file_name

    def __download_video(self, url: str, file_name: str):
        output_file = os.path.join(self.output_dir, file_name)
        try:
            if not os.path.isfile(output_file):
                response = requests.get(url, stream=True)
                if response.status_code == 200:
                    with open(output_file, 'wb') as file:
                        for chunk in response.iter_content(chunk_size=1024):
                            if chunk:
                                file.write(chunk)
                    print(f"Video downloaded successfully and saved to {output_file}")
                else:
                    print(f"Failed to download video. Status code: {response.status_code}")
        except KeyboardInterrupt:
            # If interrupted, delete the partially downloaded file
            if os.path.isfile(output_file):
                os.remove(output_file)
                print(f"Download interrupted. Partially downloaded file {output_file} has been deleted.")
            raise  # Re-raise the exception to stop the program
        except Exception as e:
            print(f"An error occurred: {e}")

    def execute(self):
        try:
            with open(self.input_csv_file, 'r', newline='', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)

                for index, row in enumerate(reader, start=2):  # 設為從2開始，方便和csv對照
                    if row['項目'] == '冷煤':
                        file_name = self.__video_name_merge(row)
                        print(f'Now Processing... {index}: {file_name}')
                        split_file_name = file_name.split('-')
                        camera_id = split_file_name[1]
                        date = split_file_name[2]
                        time_ = split_file_name[3].split('.')[0]
                        URL = f'https://cctvidentification.stantec.com.tw/Content/Upload/Video/Ref/{camera_id}/{date}-{time_}.mp4'
                        self.__download_video(url=URL, file_name=file_name)

                    else:
                        continue
                print('[VideoDownloader] All video are downloaded.')

        except KeyboardInterrupt:
            print("\n[VideoDownloader] Download interrupted by user.")



if __name__ == '__main__':
    INPUT_CSV_FILE = '202305~202309 異常事件.csv'  # 設定輸入csv的路徑
    OUTPUT_DIR = os.path.join('.', 'output')      # 設定輸出路徑

    video_downloader = VideoDownloader(input_csv_file=INPUT_CSV_FILE,
                                       output_dir=OUTPUT_DIR)
    video_downloader.execute()
