# PlayEventVideo
- 使用說明:  
    1. 將csv檔與mp4檔放入`input`內，csv為`{工廠名稱}/{日期}/{時間}/{鏡頭編號}/{csv}`裡面的`{日期}-{時間}.csv`，mp4為`{工廠名稱}/{日期}/{時間}/{鏡頭編號}/{final}`裡面的`{日期}-{時間}.mp4`，或是設定相關路徑即可自動抓取，省去移動檔案的步驟(在main設定case1 or 2的路徑，並決定要傳哪組參數)。
    2. 設定`PlayEventVideo.py`內的相關參數(main的開頭部分，filename, factory_name, camera_id)
    3. 執行`PlayEventVideo.py`
    4. 照提示輸入確認結果 (y:yes  n:no  q:exit  other:replay)
    5. 去`output`內取得`{工廠名稱}-{鏡頭編號}-{日期}-{時間}_checked.csv`即為所要的資料