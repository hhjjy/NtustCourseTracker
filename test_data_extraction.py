import sys
from course_query_system import fetch_courses, update_database, find_available_courses, create_database

def test_data_extraction():
    print("開始測試數據提取...")
    
    # 獲取課程數據
    courses = fetch_courses()
    if not courses:
        print("錯誤：無法獲取課程數據")
        return
    
    print(f"成功獲取 {len(courses)} 門課程")
    
    # 打印前5門課程的詳細信息
    print("\n前5門課程的詳細信息：")
    for course in courses[:5]:
        print(f"課程編號: {course.CourseNo}")
        print(f"課程名稱: {course.CourseName}")
        print(f"教師: {course.CourseTeacher}")
        print(f"學分: {course.CreditPoint}")
        print(f"備註: {course.CourseNotes}")
        print("---")
    
    # 創建並更新數據庫
    create_database()
    update_database(courses)
    
    # 查找可選課程
    available_courses = find_available_courses()
    print(f"\n共找到 {len(available_courses)} 門可選課程")
    
    # 打印前5門可選課程
    print("\n前5門可選課程：")
    for course in available_courses[:5]:
        print(f"課程編號: {course.CourseNo}, 名稱: {course.CourseName}, 教師: {course.CourseTeacher}, 學分: {course.CreditPoint}")

if __name__ == "__main__":
    test_data_extraction()