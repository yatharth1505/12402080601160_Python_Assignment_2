# Programming with Python — Assignment 2

**Student:** Yatahrth Mehta
**Enrollment No.:** 12402080601160

## Programs
1. Regex-Based Email Intelligence Extractor
2. Offline Web Scraping Ranker from HTML Pages
3. MySQL Student-Course Analytics Engine
4. SQL Join Query Builder and Validator
5. Tkinter Contact Manager with MySQL Backend
6. Log Anomaly Detector using Sliding Window
7. Generator-Based JSON ETL Pipeline
8. Matrix Path Optimizer with Dynamic Programming
9. OOP Inventory Merger with Operator Overloading
10. Python Data Visualization Dashboard Exporter

## Requirements
Python 3.10+. Q1, Q2, Q4, Q6-Q9 use the standard library. Q3/Q5 require `pip install mysql-connector-python`; Q10 requires `pip install matplotlib`.

## Run examples
```bash
python 12402080601160_Assignment2_Q1.py samples/emails.txt
python 12402080601160_Assignment2_Q2.py < samples/products_input.txt
python 12402080601160_Assignment2_Q3.py
python 12402080601160_Assignment2_Q4.py < samples/query.json
python 12402080601160_Assignment2_Q5.py
python 12402080601160_Assignment2_Q6.py < samples/logs.txt
python 12402080601160_Assignment2_Q7.py samples/sensors.jsonl
python 12402080601160_Assignment2_Q8.py < samples/matrix.txt
python 12402080601160_Assignment2_Q9.py < samples/inventory.json
python 12402080601160_Assignment2_Q10.py samples/marks.csv output_folder
```

## Database setup
Create `assignment2` in MySQL and set `MYSQL_HOST`, `MYSQL_USER`, `MYSQL_PASSWORD`, and `MYSQL_DATABASE` environment variables. Q3 expects `student.csv` with `student_id,name,spi` and `registration.csv` with `student_id,course_id` in the current directory.

Q2 expects product-card HTML using classes such as `product-card`, `product-name`, `price`, and `rating`; adapt selectors if your saved pages use different markup.

The assignment requests sample, boundary, and at least three additional self-created tests per program. Review and test the programs against your faculty's expected interpretation before submission.
