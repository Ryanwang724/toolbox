# toolbox各項專案簡介
>注意：建議進入各專案資料夾內執行，避免相對路徑問題。


| **專案名稱**                                           | **功能簡介**                                                                                     |
|-------------------------------------------------------|---------------------------------------------------------------------------------------------|
| [FactoryParameterToCsv](./FactoryParameterToCsv)       | 讀取工廠的參數檔，檢查是否有做 Bypass 和飽和度亮度遮罩。                                              |
| [MaskGenerateNewRoi](./MaskGenerateNewRoi)             | 將舊版 ROI 資料（Mask）轉為新版 ROI，省去人工重畫的步驟。                                            |
| [PlayEventVideo](./PlayEventVideo)                     | 進行人工複判並輸出 0 或 1 的 CSV 結果。                                                           |
| [ProcessVideoFrameFalse](./ProcessVideoFrameFalse)     | 檢查影片讀取失敗的原因並修復。                                                                    |
| [ReCheckEvent](./ReCheckEvent)                         | 確認人工複判為冷媒的真實時間點。                                                                  |
| [RoiDisplay](./RoiDisplay)                             | 顯示或存檔指定工廠鏡頭的 ROI 資料，用於觀察 ROI 繪製結果。                                            |
| [RoiDownloadFromAPI](./RoiDownloadFromAPI)             | 根據所有工廠鏡頭編號，透過傑明 API 撈取 ROI 資料。                                                  |
| [StatisticCheckedEvent](./StatisticCheckedEvent)       | 處理 `PlayEventVideo` 的輸出，產生統計結果的 CSV 與折線圖。                                           |
| [VideoClipper](./VideoClipper)                         | 根據事件時間點剪輯影片。                                                                          |
| [VideoDownloader](./VideoDownloader)                  | 從傑明網站下載對應事件的影片。                                                                     |
| [roi_from_url](./roi_from_url)                         | 從 API 獲取最新的冷媒鏡頭 ROI，可將此資料夾複製到各專案的 `input`。                                   |
| [Compare2ModelEvent.py](./Compare2ModelEvent.py)       | 此程式用於統計兩個模型（model1 和 model2）在不同工廠、日期、時間段內的事件數，並將統計結果儲存為 JSON 檔案，方便後續比較與分析。|
| [calc_roi_area.py](./calc_roi_area.py)                 | 計算各 channel 的 ROI 面積（需先修改檔案路徑）。                                                    |
| [compare_json.py](./compare_json.py)                   | 比較兩個資料夾中相同檔案名稱的 JSON 檔案，分析它們的內容差異並輸出結果(確認兩地參數檔是否相同)。|
| [compare_model_event.py](./compare_model_event.py)     | 統計多個 CSV 檔案中的模型處理結果，計算每個工廠 (factory)、攝影機 ID (camera_ID) 和頻道 (channel) 下，各模型的總事件數 (event_count) 和總運行時間 (total_run_time)，並將統計結果輸出至終端機以及儲存到新的 CSV 文件。|
| [factory_list.json](./factory_list.json)               | 最新冷媒鏡頭名單，可將此檔案複製到各專案的 `input`。                                                 |
| [maintain_data.py](./maintain_data.py)                 | 使用 `factory_list.json` 維護最外層的 `roi_from_url`，更新後可將結果複製進各專案的 `input`。             |
| [video_length_save_rate.py](./video_length_save_rate.py)| 計算各個模型使用相同影片集測試出來的片長節省率。                                                   |