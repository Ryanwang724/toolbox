# MaskGenerateNewRoi
- 使用說明:  
    1. 將舊版ROI資料夾`ref_roi`放入`input`內
    2. 將工廠名單`factory_list.json`放入`input`內
    3. 執行`MaskGenerateNewROI.py`
    4. 程式執行結束會印出`print(f"[MaskGenerateNewROI] done")`
    5. `output`內的`mask_to_roi`為新版ROI資料
    6. `output`內的`img_result`新舊版資料比較圖，左邊為舊的資料所畫出之結果，黑色為不要的地方，白色為要的

- todo list  
- [ ] 目前是透過讀取`factory_list.json`去進行轉換，或許可以改為讀取`ref_roi`內的所有.json檔進行轉換。(透過`factory_list.json`的好處是方便管理有效之鏡頭)