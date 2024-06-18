# ReCheckEvent
> 此檔為`PlayEventVideo`修改而來
- 使用說明:  
    1. 將執行`PlayEventVideo`後產生的csv檔(檔名帶有_checked後綴)最放入`input`內。
    2. 設定`ReCheckEvent.py`內的相關參數(main的開頭部分，filename, factory_name, camera_id和result_path等路徑)
    3. 執行`ReCheckEvent.py`即可確認該事件的真實時間點，方便和網站上做比對。
    4. 照提示輸入確認結果 (y:yes  n:no  q:exit  other:replay)，此結果不會存檔。