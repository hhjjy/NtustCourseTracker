import requests
import json
from dataclasses import dataclass
from typing import List, Optional
import schedule
import time
import sqlite3
from datetime import datetime

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
    
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        courses_data = response.json()
        return [Course(**course) for course in courses_data]
    else:
        print(f"Error fetching courses: {response.status_code}")
        return []

def create_or_update_database():
    conn = sqlite3.connect('courses.db')
    c = conn.cursor()
    
    # 檢查表是否存在
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='courses'")
    if c.fetchone() is None:
        # 如果表不存在，創建新表
        c.execute('''CREATE TABLE courses
                     (Semester TEXT, CourseNo TEXT PRIMARY KEY, CourseName TEXT, CourseTeacher TEXT, 
                      Dimension TEXT, CreditPoint TEXT, RequireOption TEXT, AllYear TEXT,
                      ChooseStudent INTEGER, Restrict1 TEXT, Restrict2 TEXT, ThreeStudent INTEGER,
                      AllStudent INTEGER, NTURestrict TEXT, NTNURestrict TEXT, CourseTimes TEXT,
                      PracticalTimes TEXT, ClassRoomNo TEXT, ThreeNode TEXT, Node TEXT,
                      Contents TEXT, NTU_People INTEGER, NTNU_People INTEGER, AbroadPeople INTEGER)''')
    else:
        # 如果表存在，檢查並添加缺失的列
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
    
    conn.commit()
    conn.close()

def update_database(courses: List[Course]):
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
    conn.close()

def find_available_courses() -> List[Course]:
    conn = sqlite3.connect('courses.db')
    c = conn.cursor()
    c.execute("""
        SELECT * FROM courses 
        WHERE CAST(ChooseStudent AS INTEGER) < CAST(Restrict2 AS INTEGER)
    """)
    rows = c.fetchall()
    conn.close()
    
    available_courses = []
    for row in rows:
        try:
            course_dict = dict(zip([column[0] for column in c.description], row))
            course = Course(**course_dict)
            available_courses.append(course)
        except Exception as e:
            print(f"錯誤：創建 Course 對象時發生錯誤。")
            print(f"錯誤信息：{str(e)}")
            print(f"問題數據：{course_dict}")
    
    return available_courses

import random

def query_and_process_courses():
    courses = fetch_courses()
    update_database(courses)
    available_courses = find_available_courses()
    
    print(f"總共獲取到 {len(courses)} 門課程信息")
    print(f"其中 {len(available_courses)} 門課程當前可選:")
    

    print("\n數據更新完成。")

def main():
    print("台科大課程查詢系統啟動")
    create_or_update_database()
    
    # 立即執行一次查詢
    query_and_process_courses()
    
    # 設置定期任務
    schedule.every(1).hour.do(query_and_process_courses)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()