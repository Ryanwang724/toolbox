# ProcessVideoFrameFalse
當影片幀無法被讀取時會報錯，使用`CheckFrameState.py`確認問題，視情況使用`MergeVideo.py`修復。
- 使用說明:
    1. 將欲處理的影片放入`input`內。
    2. 設定`CheckFrameState.py`內的相關路徑。
    3. 修改__plot_fig中的顯示範圍。
    4. 執行`CheckFrameState.py`。
    5. 至`output`確認結果。
    6. 依照結果決定是否執行`MergeVideo.py`。
    7. 執行`MergeVideo.py`。
    8. 至`output`取得結果影片。