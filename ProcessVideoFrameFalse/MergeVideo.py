import cv2
import os
import re
import time


class MergeVideo:
    def __process_video(self, video_path: str, output_path: str):
        start_time = time.time()
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            print(f"Can not open video: {video_path}")
            exit()

        print(f"Success open video file: {video_path}")

        # get video attribute
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_rate = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, 6.993, (frame_width, frame_height))

        success_cnt: int = 0
        total_cnt: int = 0
        while total_cnt < frame_count:
            success, frame = cap.read()
            total_cnt += 1
            if success:
                success_cnt += 1
                out.write(frame)
        
            print(f"Read {total_cnt} frame: {success}, [success/total]: {success_cnt}/{total_cnt}")
        end_time = time.time()
        print(f"frame width: {frame_width}")
        print(f"frame height: {frame_height}")
        print(f"frame rate: {frame_rate}")
        print(f"frame count: {frame_count}")
        print(f'Video process time: {round(end_time - start_time, 3)} sec.')

        cap.release()
        out.release()

    def execute(self, input_video_path: str, output_path: str):
        os.makedirs(output_path, exist_ok=True)

        file_name = re.split(r'/|\.', input_video_path)[-2] + '_processed.mp4'
        output_file_path = os.path.join(output_path, file_name)

        self.__process_video(input_video_path, output_file_path)

if __name__ == '__main__':
    VIDEO_PATH = os.path.join('.', 'input', '惠嘉電-5041528204-20240616-180000.mp4') # 修改為影片路徑
    OUTPUT_PATH = os.path.join('.', 'output') # 輸出資料夾路徑
    mv = MergeVideo()
    mv.execute(input_video_path=VIDEO_PATH, output_path=OUTPUT_PATH)