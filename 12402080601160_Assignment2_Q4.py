"""Q4 Safe SQL join query builder. Reads JSON from stdin; prints SQL and parameters."""
import json, sys
TABLES={"student":{"id":"s.student_id","name":"s.name","spi":"s.spi"},"course":{"id":"c.course_id","name":"c.name"},"registration":{"student_id":"r.student_id","course_id":"r.course_id"}}
OPS={"=","!=","<",">","<=",">=","LIKE"}
def build(data):
    def field(value):
        if not isinstance(value,str) or "." not in value: raise ValueError(f"Invalid field: {value}")
        table,col=value.split(".",1)
        if table not in TABLES or col not in TABLES[table]: raise ValueError(f"Field not allowed: {value}")
        return TABLES[table][col]
    cols=data.get("columns",["student.name","course.name"]); filters=data.get("filters",[])
    direction=str(data.get("direction","DESC")).upper(); limit=int(data.get("limit",10))
    if not isinstance(cols,list) or not cols: raise ValueError("columns must be a non-empty list")
    if direction not in {"ASC","DESC"}: raise ValueError("direction must be ASC or DESC")
    if not 1<=limit<=1000: raise ValueError("limit must be 1..1000")
    select=", ".join(field(c) for c in cols); order=field(data.get("order_by","student.spi")); where=[]; params=[]
    for f in filters:
        op=str(f.get("operator","=")).upper()
        if op not in OPS: raise ValueError(f"Unsupported operator: {op}")
        where.append(field(f.get("field"))+" "+op+" %s"); params.append(f.get("value"))
    sql=f"SELECT {select} FROM Student s JOIN CourseRegistration r ON r.student_id=s.student_id JOIN Course c ON c.course_id=r.course_id"
    if where: sql+=" WHERE "+" AND ".join(where)
    sql+=f" ORDER BY {order} {direction} LIMIT %s"; params.append(limit)
    return sql,params
def main():
    try:
        sql,params=build(json.load(sys.stdin)); print("SQL_OK"); print(sql); print("PARAMS",json.dumps(params))
    except (ValueError,TypeError,AttributeError,json.JSONDecodeError) as e: raise SystemExit(f"INVALID: {e}")
if __name__=="__main__": main()
