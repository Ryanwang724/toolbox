# toolbox各項專案簡介
盡量都進入專案資料夾內執行(相對路徑問題)

## FactoryParameterToCsv
- 讀取工廠的參數檔，印出是否有做bypass與飽和度亮度遮罩。

## RoiDownloadFromAPI
- 讀取所有工廠鏡頭編號，至傑明API撈取資料。

## RoiDisplay
- 顯示或存檔指定工廠的鏡頭ROI資料，觀察ROI繪製結果。

## MaskGenerateNewRoi
- 利用舊版ROI資料(mask)轉為新版ROI資料，省去人工重畫步驟。

## factory_list.json
- 最新之冷媒鏡頭名單，可將此檔複製進各專案之`input`。

## roi_from_url
- 從API獲取的最新之冷媒鏡頭ROI，可將此資料夾複製進各專案之`input`。