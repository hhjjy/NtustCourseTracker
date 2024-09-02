# NtustCourseTracker

這是一個用於追踪台灣科技大學課程是否可以選空的應用程序。

## 功能

- 課程查詢
- 用戶註冊和認證
- 課程追踪
- 通知系統

## 安裝

1. 確保您已安裝 pyenv 和 Python 3.12.4
2. 克隆倉庫
3. 進入專案目錄：`cd NtustCourseTracker`
4. 創建並激活虛擬環境：
   ```
   pyenv virtualenv 3.12.4 ntust-course-tracker
   pyenv local ntust-course-tracker
   ```
5. 安裝依賴：`pip install -r requirements.txt`
6. 運行遷移：`python manage.py migrate`
7. 啟動服務器：`python manage.py runserver`

## 開發

- 遵循 PEP 8 編碼規範
- 在提交前運行測試：`python manage.py test`

## 項目路線圖

1. CI/CD 部署
   - 設置服務器和 IPv6 支持
   - 配置 GitHub Actions
   - 測試部署流程

2. 核心功能開發
   - 實現定期訂閱查詢功能
   - 開發課程資訊抓取系統
   - 完善用戶認證系統

3. 推送功能
   - 設計和實現推送系統

4. 用戶界面開發
   - 創建響應式布局
   - 實現課程搜索和過濾功能
   - 設計用戶儀表板

5. API 開發
   - 設計和實現 RESTful API

6. 測試
   - 編寫單元測試和集成測試
   - 進行負載測試

7. 性能優化
   - 實現緩存機制
   - 優化數據庫查詢

8. 安全性增強
   - 實現 HTTPS
   - 加強密碼策略和安全防護

9. 文檔和說明
   - 編寫用戶指南和開發者文檔

10. 發布準備
    - 進行最終測試
    - 準備發布說明

## 貢獻

歡迎提交 pull requests。對於重大更改，請先開 issue 討論您想要更改的內容。

## 授權

[MIT](https://choosealicense.com/licenses/mit/)