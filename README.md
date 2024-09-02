# NtustCourseTracker

這是一個用於追踪台灣科技大學課程的應用程序。

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

## 貢獻

歡迎提交 pull requests。對於重大更改，請先開 issue 討論您想要更改的內容。

## 授權

[MIT](https://choosealicense.com/licenses/mit/)