import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import json
import os
import cv2
import numpy as np

class RoiDisplayer:

    # 請先修改此區參數================================
    JSON_FILE_NAME = "聯榮-5072141805.json"
    SHOW_OR_SAVE = False  # True:show ; False:save
    # 請先修改此區參數================================

    def __init__(self):
        self.input_path = f'./input/roi_from_url/{self.JSON_FILE_NAME}'
        self.output_path = './output'
        self.roi_data = dict()
        self.is_split = None
    
    def get_area_point_list(self, channel):
        area_list = []
        for each_area in self.roi_data[channel]:
            area_tmp = []
            for each_point in each_area:
                area_tmp.append([each_point[0], each_point[1]])
            area_list.append(np.array(area_tmp))
        return area_list

    def read_file(self):
        with open(self.input_path ,mode='r',encoding='utf-8') as f:
            json_data = json.load(f)
        self.roi_data = json_data["roi_data"]
        self.is_split = json_data["is_split"]

    def check_dir_exist(self):
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)
        if not os.path.exists(self.input_path):
            os.makedirs(self.input_path)

    def execute(self):
        self.check_dir_exist()
        self.read_file()
        if self.is_split is True:
            frame_x = 360
            frame_y = 240
            fig, axs = plt.subplots(2, 2, figsize=(10, 8))
            for idx, (channel, data) in enumerate(self.roi_data.items()):
                ax = axs[idx // 2, idx % 2]
                ax.set_xlim(0, frame_x)
                ax.set_ylim(frame_y, 0)
                ax.set_aspect('equal')
                ax.set_title(channel)
                
                if data:
                    self.area_list = self.get_area_point_list(channel)
                    Area_mask = np.zeros((frame_y,frame_x,3),dtype=np.uint8)
                    cv2.fillPoly(Area_mask, self.area_list,(255,255,255))
                    cv2.polylines(Area_mask, self.area_list, True, (255, 0, 0), 1)
                    ax.imshow(Area_mask)
                else:
                    empty_fig = np.zeros((frame_y,frame_x,3),dtype=np.uint8)
                    empty_fig[:,:,:] = 255 
                    ax.plot([0, frame_x], [0, frame_y], 'r-', linewidth=2)  # 左上到右下
                    ax.plot([0, frame_x], [frame_y, 0], 'r-', linewidth=2)  # 左下到右上
        else:
            frame_x = 720
            frame_y = 480
            fig, ax = plt.subplots(figsize=(10, 8))
            channel, data = next(iter(self.roi_data.items()))
            ax.set_xlim(0, 720)
            ax.set_ylim(480, 0)
            ax.set_title(channel)
            
            if data:
                self.area_list = self.get_area_point_list(channel)
                Area_mask = np.zeros((frame_y,frame_x,3),dtype=np.uint8)
                cv2.fillPoly(Area_mask, self.area_list,(255,255,255))
                cv2.polylines(Area_mask, self.area_list, True, (255, 0, 0), 2)
                ax.imshow(Area_mask)

        plt.tight_layout()

        file_name = self.JSON_FILE_NAME.split('.')[0]
        if self.SHOW_OR_SAVE:
            plt.show()
            print(f"[RoiDisplayer] [{file_name}] show fig done")
        else: 
            plt.savefig(f'{self.output_path}/{file_name}.png')
            print(f"[RoiDisplayer] [{file_name}] save fig done")

if __name__ == '__main__':
    rd = RoiDisplayer()
    rd.execute()