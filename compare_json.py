import os
import json
from deepdiff import DeepDiff

def compare_json_files(folder1, folder2):
    # 列出兩個資料夾中的所有檔案
    files1 = set(os.listdir(folder1))
    files2 = set(os.listdir(folder2))
    
    # 找出兩個資料夾都有的檔案
    common_files = files1.intersection(files2)
    
    # 比較每個共同的檔案
    for file_name in common_files:
        file_path1 = os.path.join(folder1, file_name)
        file_path2 = os.path.join(folder2, file_name)
        
        # 打開並讀取 JSON 檔案
        with open(file_path1, 'r', encoding='utf-8') as f1, open(file_path2, 'r', encoding='utf-8') as f2:
            json1 = json.load(f1)
            json2 = json.load(f2)
        
        # 使用 DeepDiff 來比較兩個 JSON 的差異
        diff = DeepDiff(json1, json2, ignore_order=True)
        
        if diff:
            print(f"檔案 {file_name} 存在差異:")
            print(diff)
        else:
            print(f"檔案 {file_name} 沒有差異")

# 資料夾路徑
folder1 = '/home/ryan/nas/nas_ryan/EPA-Dissipation/code/AllParameter/Factory_parameter'
folder2 = '/home/ryan/nas/nas_ryan/EPA-Dissipation/code/AllParameter_0911_stantec_server/Factory_parameter'

compare_json_files(folder1, folder2)
