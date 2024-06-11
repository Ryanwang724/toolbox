import numpy as np
import cv2
import json
import os

class MaskGenerateNewROI:
    """利用mask之資料產生新的ROI資料
    """
    def __init__(self, save_mode :bool, pixel_threshold :int):
        self.area_list = []
        self.frame_x = 360
        self.frame_y = 240
        self.pixel_threshold = pixel_threshold
        self.this_file_dir = os.path.dirname(os.path.abspath(__file__))
        self.input_path = os.path.join(self.this_file_dir, 'input', 'ref_roi')
        self.output_path = os.path.join(self.this_file_dir, 'output')
        self.roi_dest_path = os.path.join(self.output_path, 'mask_to_roi')
        self.img_dest_path = os.path.join(self.output_path, 'img_result')
        self.camera_list_file = os.path.join(self.this_file_dir, 'input', 'factory_list.json')

        self.run_list = [] # 要跑的工廠與camera id ex: [['久發', '5071930202']]
        self.roi_file = {}
        self.save_mode = save_mode
        self.save_data = {"is_split": None, "channel": None, "roi_data": {"channel1": [], "channel2": [], "channel3": [], "channel": []}}
        
    def get_run_list(self):      # run_list = [ ['工廠名稱','cam id'], ['工廠名稱','cam id'] ]
        with open(self.camera_list_file,'r',encoding='utf-8') as f:
            json_data = json.load(f)
            for num, info in json_data.items():
                info = info.split('-')
                self.run_list.append(info)

    def set_frame_size(self):   # 確認畫面大小 for 綠環境 special case  
        if self.roi_file.get('is_split'):
            self.frame_x = 360
            self.frame_y = 240
        else:      
            self.frame_x = 720
            self.frame_y = 480

    def check_dir_exist(self):
        if not os.path.exists(self.input_path):
            os.makedirs(self.input_path)
        if not os.path.exists(self.roi_dest_path):
            os.makedirs(self.roi_dest_path)
        if not os.path.exists(self.img_dest_path):
            os.makedirs(self.img_dest_path)

    def generate_new_roi_data(self, inverted_mask):
        contours, _ = cv2.findContours(inverted_mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        roi_data = []

        for contour in contours:
            roi = contour.squeeze().tolist()
            roi_data.append(roi)

        return roi_data

    def get_area_point_list(self, channel_index: int): 
        for each_area in self.roi_file["roi_data"]["channel"+str(channel_index)]:
            area_tmp = []
            for each_point in each_area:

                if each_point[0] > self.frame_x:                           # 超出範圍拉回
                    each_point[0] = self.frame_x-1
                if each_point[0] < 0:
                    each_point[0] = 0
                if each_point[1] > self.frame_y:
                    each_point[1] = self.frame_y-1
                if each_point[1] < 0:
                    each_point[1] = 0
                

                if (self.frame_x - each_point[0]) < self.pixel_threshold:  # 太貼近邊界=>拉至邊界
                    each_point[0] = self.frame_x-1
                if each_point[0] < self.pixel_threshold:
                    each_point[0] = 0
                if (self.frame_y - each_point[1]) < self.pixel_threshold:
                    each_point[1] = self.frame_y-1
                if each_point[1] < self.pixel_threshold:
                    each_point[1] = 0

                area_tmp.append([each_point[0], each_point[1]])
            self.area_list.append(np.array(area_tmp))

    def execute(self):
        self.check_dir_exist() # 檢查img存檔位置

        self.get_run_list()
        for data in self.run_list:  # 一次跑一間工廠
            read_file_path = os.path.join(self.input_path, f'{data[0]}-{data[1]}.json')
            with open(read_file_path,'r',encoding='utf-8') as f:
                self.roi_file = json.load(f)
            self.set_frame_size()
            run_channel = self.roi_file.get('channel') # 要跑哪些channel
            for ch in run_channel:
                self.area_list = []
                self.get_area_point_list(channel_index=ch)

                area_mask = np.zeros((self.frame_y,self.frame_x),dtype=np.uint8)
                cv2.fillPoly(area_mask, self.area_list,255)                      # 生成mask

                mask_to_roi = cv2.bitwise_not(area_mask)                         # 正確ROI之區域

                new_roi = self.generate_new_roi_data(mask_to_roi)   # 用正確之ROI區域產生新的ROi file
                self.area_list = []
                for each_area in new_roi:
                    area_tmp = []
                    for each_point in each_area:
                        area_tmp.append([each_point[0], each_point[1]])
                    self.area_list.append(np.array(area_tmp))

                new_frame = np.zeros((self.frame_y,self.frame_x),dtype=np.uint8)    # 繪製新的ROI效果
                cv2.fillPoly(new_frame, self.area_list,255)   # 生成新ROI mask

                if self.save_mode:     # save result image
                    area_mask_add_border=cv2.copyMakeBorder(area_mask,10,10,10,10,cv2.BORDER_CONSTANT,value=128)
                    new_frame_add_border=cv2.copyMakeBorder(new_frame,10,10,10,10,cv2.BORDER_CONSTANT,value=128)
                    combined_image = cv2.hconcat([area_mask_add_border, new_frame_add_border])

                    cv2.imencode('.jpg', combined_image)[1].tofile(os.path.join(self.img_dest_path, f'/{data[0]}-{data[1]}_channel{ch}.jpg'))

                self.save_data = self.roi_file       # maintain roi file
                self.save_data['roi_data'][f'channel{ch}'] = new_roi

            write_file_path = os.path.join(self.roi_dest_path, f'/{data[0]}-{data[1]}.json')
            with open(write_file_path,'w',encoding='utf-8') as fp:
                json.dump(self.save_data,fp)

        print(f"[MaskGenerateNewROI] done")

    def test(self, frame_x=360, frame_y=240, roi_path='./input/ref_roi',run_list = [['綠電楊梅廠', '5004517214']]):
        """單一工廠測試用，僅會顯示圖片，不會存檔

        使用前請先設定變數，主要為run_list和frame_x和frame_y
        """
        area_list = []
        # =======================================
        frame_x = frame_x
        frame_y = frame_y
        roi_path = roi_path
        run_list = run_list
        # =======================================
        roi_file = {}
        run_channel = []
        pixel_threshold = 20

        def generate_roi_data_from_mask(inverted_mask):
            contours, _ = cv2.findContours(inverted_mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            roi_data = []

            for contour in contours:
                roi = contour.squeeze().tolist()
                roi_data.append(roi)

            return roi_data

        for data in run_list:
            with open(roi_path+f'/{data[0]}-{data[1]}.json','r',encoding='utf-8') as f: # 讀取個別json
                roi_file = json.load(f)
            run_channel = roi_file.get('channel') # 要跑那些channel
            for ch in run_channel:
                area_list = []

                for each_area in roi_file["roi_data"]["channel"+str(ch)]: # 取得channel的點數  copy from RoiFileCreator.py def get_area_point_list()
                    area_tmp = []
                    for each_point in each_area:

                        if each_point[0] > self.frame_x:                           # 超出範圍拉回
                            each_point[0] = self.frame_x-1
                        if each_point[0] < 0:
                            each_point[0] = 0
                        if each_point[1] > self.frame_y:
                            each_point[1] = self.frame_y-1
                        if each_point[1] < 0:
                            each_point[1] = 0

                        if (frame_x - each_point[0]) < pixel_threshold:
                            each_point[0] = frame_x-1
                        if each_point[0] < pixel_threshold:
                            each_point[0] = 0
                        if (frame_y - each_point[1]) < pixel_threshold:
                            each_point[1] = frame_y-1
                        if each_point[1] < pixel_threshold:
                            each_point[1] = 0

                        area_tmp.append([each_point[0], each_point[1]])
                    area_list.append(np.array(area_tmp))
                
                area_mask = np.zeros((frame_y,frame_x),dtype=np.uint8)
                cv2.fillPoly(area_mask, area_list,255)                  # 生成mask

                mask_to_roi = cv2.bitwise_not(area_mask)

                cv2.imshow("Original Mask", area_mask)
                cv2.imshow("Inverted Mask", mask_to_roi)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                new_roi = generate_roi_data_from_mask(mask_to_roi)
                print(f'new roi:\n    {new_roi}')
        
                area_list = []
                for each_area in new_roi:
                    area_tmp = []
                    for each_point in each_area:
                        area_tmp.append([each_point[0], each_point[1]])
                    area_list.append(np.array(area_tmp))

                print(area_list)

                area_mask = np.zeros((frame_y,frame_x),dtype=np.uint8)
                cv2.fillPoly(area_mask, area_list,255)   # 生成新ROI mask
                cv2.imshow("new ROI's mask", area_mask)
                cv2.waitKey(0)
                cv2.destroyAllWindows()


if __name__ == '__main__':
    mgnr = MaskGenerateNewROI(save_mode=True, pixel_threshold=12)
    # mgnr.test(frame_x=360, frame_y=240, roi_path='./input/ref_roi',run_list = [['綠電楊梅廠', '5004517214']])  # 測試單一工廠用 請修改相關參數
    mgnr.execute()