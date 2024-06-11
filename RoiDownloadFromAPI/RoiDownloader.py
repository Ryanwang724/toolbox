import requests
import json
import os

class RoiDownloader:    
    """從傑明開放之api下載roi檔案至本地端
    """
    def __init__(self, input_path='./input/factory_list.json', output_path='./output/roi_from_url'):
        self.source_url = "https://cctvidentification.stantec.com.tw/api/CCTV/GetROIOfDetection?AuditItem=1&CameraID="
        self.output_path = output_path
        self.input_path = input_path

    def load_from_url(self,source:str):
        try:
            res = requests.get(source)
            if res.status_code == 200:
                roi_file = res.json()
            else:
                print("No corresponding roi file")
                return None
        except:
            print("[Roi FileCreater] Something Wrong")
            exit()
        else:
            return roi_file

    def check_dir_exist(self):
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)
        if not os.path.exists(self.input_path):
            os.makedirs(self.input_path)

    def save_to_file(self):
        with open(self.input_path, mode='r', encoding='utf-8') as f:
            factory_data = json.load(f)
            for num, info in factory_data.items():
                source = self.source_url + info.split('-')[1]
                roi_file = self.load_from_url(source)
                if roi_file is not None:
                    print(f"{num}. {info}:")
                    print(f"    {roi_file}\n")
                    with open(f'{self.output_path}/{info}.json', mode='w') as fp:
                        json.dump(roi_file,fp,indent=2)

    def execute(self):
        self.check_dir_exist()
        self.save_to_file()
        print('[RoiDownloader] done')

if __name__ == '__main__':
    downloader = RoiDownloader()
    downloader.execute()