import requests
import json
from dataclasses import dataclass
from typing import List, Optional
import schedule
import time
import sqlite3
from datetime import datetime
import logging
import os

# 設置日誌
log_dir = os.environ.get('LOG_DIR', '/app/logs')
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    filename=f'{log_dir}/course_query.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@dataclass
class Course:
    Semester: str
    CourseNo: str
    CourseName: str
    CourseTeacher: str
    Dimension: str
    CreditPoint: str
    RequireOption: str
    AllYear: str
    ChooseStudent: int
    Restrict1: str
    Restrict2: str
    ThreeStudent: int
    AllStudent: int
    NTURestrict: str
    NTNURestrict: str
    CourseTimes: str
    PracticalTimes: str
    ClassRoomNo: str
    ThreeNode: str
    Node: str
    Contents: str
    NTU_People: int
    NTNU_People: int
    AbroadPeople: int

def fetch_courses() -> List[Course]:
    url = "https://querycourse.ntust.edu.tw/querycourse/api/courses"
    payload = {
        "Semester": "1131",
        "CourseNo": "",
        "CourseName": "",
        "CourseTeacher": " ",
        "Dimension": "",
        "CourseNotes": "",
        "ForeignLanguage": 0,
        "OnlyGeneral": 0,
        "OnleyNTUST": 0,
        "OnlyMaster": 0,
        "OnlyUnderGraduate": 0,
        "OnlyNode": 0,
        "Language": "zh"
    }
    
    try:
        logging.info("開始獲取課程數據")
        response = requests.post(url, json=payload)
        response.raise_for_status()
        courses_data = response.json()
        logging.info(f"成功獲取 {len(courses_data)} 門課程")
        return [Course(**course) for course in courses_data]
    except requests.RequestException as e:
        logging.error(f"獲取課程時發生錯誤: {str(e)}")
        return []

def create_or_update_database():
    conn = None
    try:
        conn = sqlite3.connect('courses.db')
        c = conn.cursor()
        
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='courses'")
        if c.fetchone() is None:
            logging.info("創建新的課程表")
            c.execute('''CREATE TABLE courses
                         (Semester TEXT, CourseNo TEXT PRIMARY KEY, CourseName TEXT, CourseTeacher TEXT, 
                          Dimension TEXT, CreditPoint TEXT, RequireOption TEXT, AllYear TEXT,
                          ChooseStudent INTEGER, Restrict1 TEXT, Restrict2 TEXT, ThreeStudent INTEGER,
                          AllStudent INTEGER, NTURestrict TEXT, NTNURestrict TEXT, CourseTimes TEXT,
                          PracticalTimes TEXT, ClassRoomNo TEXT, ThreeNode TEXT, Node TEXT,
                          Contents TEXT, NTU_People INTEGER, NTNU_People INTEGER, AbroadPeople INTEGER)''')
        else:
            logging.info("檢查並更新現有課程表")
            existing_columns = [column[1] for column in c.execute("PRAGMA table_info(courses)").fetchall()]
            expected_columns = [
                'Semester', 'CourseNo', 'CourseName', 'CourseTeacher', 'Dimension', 'CreditPoint',
                'RequireOption', 'AllYear', 'ChooseStudent', 'Restrict1', 'Restrict2', 'ThreeStudent',
                'AllStudent', 'NTURestrict', 'NTNURestrict', 'CourseTimes', 'PracticalTimes',
                'ClassRoomNo', 'ThreeNode', 'Node', 'Contents', 'NTU_People', 'NTNU_People',
                'AbroadPeople'
            ]
            for column in expected_columns:
                if column not in existing_columns:
                    c.execute(f"ALTER TABLE courses ADD COLUMN {column} TEXT")
                    logging.info(f"添加新列: {column}")
        
        conn.commit()
        logging.info("數據庫表創建或更新成功")
    except sqlite3.Error as e:
        logging.error(f"數據庫操作錯誤: {str(e)}")
    finally:
        if conn:
            conn.close()

def update_database(courses: List[Course]):
    conn = None
    try:
        conn = sqlite3.connect('courses.db')
        c = conn.cursor()
        
        for course in courses:
            c.execute('''INSERT OR REPLACE INTO courses 
                         (Semester, CourseNo, CourseName, CourseTeacher, Dimension, CreditPoint, 
                          RequireOption, AllYear, ChooseStudent, Restrict1, Restrict2, ThreeStudent,
                          AllStudent, NTURestrict, NTNURestrict, CourseTimes, PracticalTimes, 
                          ClassRoomNo, ThreeNode, Node, Contents, NTU_People, NTNU_People, 
                          AbroadPeople)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                      (course.Semester, course.CourseNo, course.CourseName, course.CourseTeacher,
                       course.Dimension, course.CreditPoint, course.RequireOption, course.AllYear,
                       course.ChooseStudent, course.Restrict1, course.Restrict2, course.ThreeStudent,
                       course.AllStudent, course.NTURestrict, course.NTNURestrict, course.CourseTimes,
                       course.PracticalTimes, course.ClassRoomNo, course.ThreeNode, course.Node,
                       course.Contents, course.NTU_People, course.NTNU_People, course.AbroadPeople))
        
        conn.commit()
        logging.info(f"成功更新 {len(courses)} 門課程到數據庫")
    except sqlite3.Error as e:
        logging.error(f"更新數據庫時發生錯誤: {str(e)}")
    finally:
        if conn:
            conn.close()

def find_available_courses() -> List[Course]:
    conn = None
    try:
        conn = sqlite3.connect('courses.db')
        c = conn.cursor()
        c.execute("""
            SELECT * FROM courses 
            WHERE CAST(ChooseStudent AS INTEGER) < CAST(Restrict2 AS INTEGER)
        """)
        rows = c.fetchall()
        
        available_courses = []
        for row in rows:
            try:
                course_dict = dict(zip([column[0] for column in c.description], row))
                course = Course(**course_dict)
                available_courses.append(course)
            except Exception as e:
                logging.error(f"創建 Course 對象時發生錯誤: {str(e)}")
                logging.error(f"問題數據: {course_dict}")
        
        logging.info(f"找到 {len(available_courses)} 門可選課程")
        return available_courses
    except sqlite3.Error as e:
        logging.error(f"查詢可選課程時發生錯誤: {str(e)}")
        return []
    finally:
        if conn:
            conn.close()

def query_and_process_courses():
    logging.info("開始查詢和處理課程")
    courses = fetch_courses()
    update_database(courses)
    available_courses = find_available_courses()
    
    logging.info(f"總共獲取到 {len(courses)} 門課程信息")
    logging.info(f"其中 {len(available_courses)} 門課程當前可選")
    
    # 這裡可以添加更多的處理邏輯，比如發送通知等
    
    logging.info("數據更新完成")

def main():
    logging.info("台科大課程查詢系統啟動")
    create_or_update_database()
    
    # 立即執行一次查詢
    query_and_process_courses()
    
    # 設置定期任務
    schedule.every(1).hour.do(query_and_process_courses)
    
    logging.info("開始定期任務")
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except Exception as e:
            logging.error(f"執行定期任務時發生錯誤: {str(e)}")
            time.sleep(1800)  # 發生錯誤時等待30分鐘後繼續

if __name__ == "__main__":
    main()