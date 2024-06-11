import numpy as np
import cv2
import json

#                      修改以下區域
# ============================================================
input_path = "../EPA-Dissipation/code/AllParameter/ref_roi/"
file_name = "可百勝-5041527102.json"
# ============================================================
ROIFile_path = input_path + file_name


def ROIarea(ROIFile_path):
        """依據傳入的channel num去獲取ROI資料，計算面積後回傳

        Args:
            channel (int): channel

        Returns:
            float: 回傳面積
        """
        with open(ROIFile_path) as f:
            b = json.load(f)

        channel_list = b["channel"]

        area_dict = dict()
        for ch in channel_list:
            temp_area = 0
            for roi in b["roi_data"]["channel" + str(ch)]:
                contour = np.array(roi)
                temp_area += cv2.contourArea(contour)
                area_dict[ch] = temp_area
        return area_dict

area_dict = ROIarea(ROIFile_path)

print(file_name)
for chan,area in area_dict.items():
    print(f'    channel: {chan} area: {area}')