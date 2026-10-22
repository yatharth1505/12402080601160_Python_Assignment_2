"""Q6 Log anomaly detector. Input: X T, n, then timestamp user ip FAIL|SUCCESS lines."""
import re,sys
from collections import defaultdict,deque
LOG=re.compile(r"^(\d{2}:\d{2})\s+([A-Za-z0-9_.-]+)\s+(\d{1,3}(?:\.\d{1,3}){3})\s+(FAIL|SUCCESS)$")
def minute(s):
    h,m=map(int,s.split(":"))
    if not 0<=h<=23 or not 0<=m<=59: raise ValueError("Invalid time")
    return h*60+m
def detect(x,t,lines):
    fails=defaultdict(deque); found={}
    for line in lines:
        match=LOG.fullmatch(line.strip())
        if not match: raise ValueError(f"Invalid log line: {line}")
        stamp,user,ip,status=match.groups(); now=minute(stamp); q=fails[user]
        while q and now-q[0][0]>t: q.popleft()
        if status=="FAIL": q.append((now,ip))
        elif len(q)>=x and any(old_ip!=ip for _,old_ip in q): found.setdefault(user,stamp)
    return found
def main():
    lines=[x.strip() for x in sys.stdin if x.strip()]
    try:
        x,t=map(int,lines[0].split()); n=int(lines[1]); logs=lines[2:2+n]
        if x<1 or t<1 or len(logs)!=n: raise ValueError("Invalid X, T or record count")
        for user,stamp in sorted(detect(x,t,logs).items()): print(user,stamp)
    except (ValueError,IndexError) as e: raise SystemExit(f"Input error: {e}")
if __name__=="__main__": main()
