"""Q3 MySQL student-course analytics. pip install mysql-connector-python.
CSV headers: student_id,name,spi and student_id,course_id."""
import csv, os, sys
import mysql.connector
from mysql.connector import Error

def setup(db):
    cur=db.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS Student(student_id VARCHAR(30) PRIMARY KEY,name VARCHAR(100) NOT NULL,spi DECIMAL(3,1) NOT NULL)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS CourseRegistration(student_id VARCHAR(30) NOT NULL,course_id VARCHAR(30) NOT NULL,PRIMARY KEY(student_id,course_id),FOREIGN KEY(student_id) REFERENCES Student(student_id),INDEX idx_course(course_id))""")
    db.commit(); cur.close()

def import_csv(db):
    cur=db.cursor()
    with open("student.csv",newline="",encoding="utf-8") as f:
        for r in csv.DictReader(f):
            spi=float(r["spi"])
            if not r["student_id"].strip() or not r["name"].strip() or not 0<=spi<=10: raise ValueError(f"Invalid student row: {r}")
            cur.execute("INSERT INTO Student VALUES(%s,%s,%s) ON DUPLICATE KEY UPDATE name=VALUES(name),spi=VALUES(spi)",(r["student_id"].strip(),r["name"].strip(),spi))
    with open("registration.csv",newline="",encoding="utf-8") as f:
        for r in csv.DictReader(f):
            cur.execute("INSERT IGNORE INTO CourseRegistration VALUES(%s,%s)",(r["student_id"].strip(),r["course_id"].strip()))
    db.commit(); cur.close()

def main():
    db=None
    try:
        db=mysql.connector.connect(host=os.getenv("MYSQL_HOST","localhost"),user=os.getenv("MYSQL_USER","root"),password=os.getenv("MYSQL_PASSWORD",""),database=os.getenv("MYSQL_DATABASE","assignment2"))
        setup(db); import_csv(db)
        course=input("Course ID: ").strip(); threshold=float(input("SPI threshold: "))
        if not 0<=threshold<=10: raise ValueError("SPI must be between 0 and 10.")
        cur=db.cursor(); cur.execute("SELECT s.student_id,s.name,s.spi,r.course_id FROM Student s JOIN CourseRegistration r ON r.student_id=s.student_id WHERE r.course_id=%s AND s.spi>%s ORDER BY s.spi DESC,s.student_id ASC",(course,threshold))
        for row in cur: print(row[0],row[1],float(row[2]),row[3])
        cur.close()
    except (Error,OSError,ValueError,KeyError) as e: raise SystemExit(f"Error: {e}")
    finally:
        if db and db.is_connected(): db.close()
if __name__=="__main__": main()
