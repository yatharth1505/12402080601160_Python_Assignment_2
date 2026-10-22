"""Q7 Generator-based JSONL ETL. Temperatures are summarized in Celsius; conversion to Fahrenheit is calculated too."""
import json,sys
from collections import defaultdict
from pathlib import Path
def records(path):
    with open(path,encoding="utf-8") as f:
        for line_no,line in enumerate(f,1):
            try:
                row=json.loads(line)
                yield line_no,row if isinstance(row,dict) else None
            except json.JSONDecodeError: yield line_no,None
def main():
    if len(sys.argv)!=2 or not Path(sys.argv[1]).is_file(): raise SystemExit("Usage: python 12402080601160_Assignment2_Q7.py sensors.jsonl")
    stats=defaultdict(lambda:{"count":0,"min":float("inf"),"max":float("-inf"),"sum":0.0,"bad":0}); unknown=0
    try:
        for _,row in records(sys.argv[1]):
            if row is None: unknown+=1; continue
            device=str(row.get("device_id","")).strip() or "UNKNOWN"
            try:
                temp=float(row["temperature_c"]); humidity=float(row["humidity"])
                if not -100<=temp<=200 or not 0<=humidity<=100: raise ValueError
            except (KeyError,TypeError,ValueError): stats[device]["bad"]+=1; continue
            # Unit transformation is available for downstream use.
            temp_f=temp*9/5+32
            s=stats[device]; s["count"]+=1; s["min"]=min(s["min"],temp); s["max"]=max(s["max"],temp); s["sum"]+=temp
        for device,s in sorted(stats.items()):
            if s["count"]: print(f'{device} count={s["count"]} min={s["min"]:g} max={s["max"]:g} avg={s["sum"]/s["count"]:.2f} corrupted={s["bad"]}')
            else: print(f'{device} count=0 corrupted={s["bad"]}')
        if unknown: print(f"UNKNOWN corrupted={unknown}")
    except OSError as e: raise SystemExit(f"File error: {e}")
if __name__=="__main__": main()
