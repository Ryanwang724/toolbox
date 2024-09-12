import cv2
import os
import time
import matplotlib.pyplot as plt


class CheckFrameState:
    def __check_video_file(self, video_path: str):
        if not os.path.exists(video_path):
            print(f"file not exist: {video_path}")
            return False
        return True

    def __plot_fig(self, result_list: list, total_cnt: int, output_path: str):
        # plot result
        plt.figure(figsize=(10, 5))

        # plot all frame is too difficult to see result (fail frequency is very high)
        plt.plot(range(1, 100 + 1), result_list[:100], marker='o', linestyle='-', color='b')    # only plot first 100 data
        # plt.plot(range(1, total_cnt + 1), result_list, marker='o', linestyle='-', color='b')  # plot all data

        plt.xlabel('Frame Index')
        plt.ylabel('Read Success (0) / Failure (1)')
        plt.title('Frame Read Success and Failure Over Time')
        plt.grid(True)

        path = os.path.join(output_path, 'result.png')
        plt.savefig(path, transparent = True)


    def execute(self, input_video_path: str, output_path: str):
        if not self.__check_video_file(input_video_path):
            exit()

        os.makedirs(output_path, exist_ok=True)

        start_time = time.time()
        cap = cv2.VideoCapture(input_video_path)

        if not cap.isOpened():
            print(f"Can not open video: {input_video_path}")
            exit()
        
        print(f"Success open video file: {input_video_path}")

        # get video attribute
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_rate = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        success_cnt: int = 0
        total_cnt: int = 0
        result_list: list = []
        while total_cnt < frame_count:
            success, frame = cap.read()
            total_cnt += 1

            if success:
                success_cnt += 1
                result_list.append(0)
            else:
                result_list.append(1)

            print(f"Read {total_cnt} frame: {success}, [success/total]: {success_cnt}/{total_cnt}")
        end_time = time.time()
        print(f"frame width: {frame_width}")
        print(f"frame height: {frame_height}")
        print(f"frame rate: {frame_rate}")
        print(f"frame count: {frame_count}")
        print(f'Video read time: {round(end_time - start_time, 3)} sec.')

        cap.release()

        self.__plot_fig(result_list, total_cnt, output_path)


if __name__ == '__main__':
    VIDEO_PATH = os.path.join('.', 'input', '惠嘉電-5041528204-20240616-180000.mp4') # 修改為影片路徑
    OUTPUT_PATH = os.path.join('.', 'output') # 輸出資料夾路徑
    cfs = CheckFrameState()
    cfs.execute(input_video_path=VIDEO_PATH, output_path=OUTPUT_PATH)