import os
import json
import csv

class ReadFactoryParameter:
    def __init__(self):
        self.this_file_dir = os.path.dirname(os.path.abspath(__file__))
        self.input_path = os.path.join(self.this_file_dir, 'input', 'Factory_parameter')
        self.output_path = os.path.join(self.this_file_dir, 'output')
        self.save_data = list()

    def load_all_file(self, fileExt: str):
        # list內只有指定附檔名的檔案，排除資料夾
        all_file_list = [f for f in os.listdir(self.input_path) if os.path.isfile(os.path.join(self.input_path, f)) and f.endswith(fileExt)]
        return all_file_list

    def check_dir_exist(self):
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)
        if not os.path.exists(self.input_path):
            os.makedirs(self.input_path)

    def csv_title_format(self):
        return ['factory_Name', 'camid', 'channel', 'bypass', 'area_threshold', 'time_threshold',
                'do_saturation', 'saturation_threshold', 'do_brightness', 'brightness_threshold']

    def write_csv(self, data: list, mode: str):
        file_path = os.path.join(self.output_path, 'result.csv')
        with open(file_path, mode, encoding='utf-8-sig', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(data)

    def execute(self):
        all_file_list = self.load_all_file('.json')
        # print(all_file_list)

        self.check_dir_exist() # 創建資料夾

        title = self.csv_title_format()
        self.write_csv(title,'w')  # 寫入標題欄位

        for file in all_file_list:
            file_path = os.path.join(self.input_path, file)
            with open(file_path,'r',encoding='utf-8') as f:
                json_file = json.load(f)
                for cam_ in json_file.get('cam'): # 個別的相機
                    temp_list = []
                    temp_list.append(json_file.get('factory_Name'))
                    for name in self.csv_title_format()[1:]: # 跳過factory_Name
                        temp_list.append(cam_.get(name))
                    self.write_csv(temp_list,'a')

        print('[ReadFactoryParameter] done')

if __name__ == '__main__':
    test = ReadFactoryParameter()
    test.execute()