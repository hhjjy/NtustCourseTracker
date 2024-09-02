import unittest
from course_query_system import fetch_courses

class TestCourseAPI(unittest.TestCase):

    def test_api_connection_and_data(self):
        print("正在測試 API 連接和數據獲取...")
        courses = fetch_courses()
        
        # 檢查是否成功獲取到課程數據
        self.assertIsNotNone(courses, "未能從 API 獲取數據")
        
        # 檢查獲取到的課程數量是否大於 0
        course_count = len(courses)
        self.assertGreater(course_count, 0, f"API 返回了 {course_count} 門課程，預期應大於 0")
        
        print(f"成功從 API 獲取到 {course_count} 門課程")

if __name__ == '__main__':
    unittest.main()