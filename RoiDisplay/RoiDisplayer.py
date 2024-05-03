import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import json
import os

class RoiDisplayer:

    # 請先修改此區參數================================
    JSON_FILE_NAME = "弘光-5071927718.json"
    SHOW_OR_SAVE = False  # True:show ; False:save
    # 請先修改此區參數================================

    def __init__(self):
        self.input_path = f'./input/roi_from_url/{self.JSON_FILE_NAME}'
        self.output_path = './output'
        self.roi_data = dict()
        self.is_split = None
    
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
            fig, axs = plt.subplots(2, 2, figsize=(10, 8))
            for idx, (channel, data) in enumerate(self.roi_data.items()):
                if data:
                    ax = axs[idx // 2, idx % 2]
                    ax.set_xlim(0, 360)
                    ax.set_ylim(240, 0)
                    ax.set_title(channel)
                    for poly in data:
                        ax.add_patch(Polygon(poly, closed=True, fill='b', edgecolor='r'))
        else:
            fig, ax = plt.subplots(figsize=(10, 8))
            channel, data = next(iter(self.roi_data.items()))
            ax.set_xlim(0, 720)
            ax.set_ylim(480, 0)
            ax.set_title(channel)
            for poly in data:
                ax.add_patch(Polygon(poly, closed=True, fill='b', edgecolor='r'))

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