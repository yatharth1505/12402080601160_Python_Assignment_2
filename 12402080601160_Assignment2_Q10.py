"""Q10 CSV cleaning and chart exporter. Install matplotlib."""
import csv,sys
from pathlib import Path
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
except ImportError: raise SystemExit("Install matplotlib: pip install matplotlib")
def load(path):
    with open(path,newline="",encoding="utf-8") as f:
        reader=csv.DictReader(f)
        if not reader.fieldnames or "name" not in reader.fieldnames:raise ValueError("CSV must contain name column")
        subjects=[x for x in reader.fieldnames if x not in {"enrollment","name"}]
        rows=[]
        for r in reader:
            item={"enrollment":r.get("enrollment","").strip(),"name":r.get("name","").strip()}
            marks=[]
            for sub in subjects:
                try:v=float(r[sub]) if (r.get(sub) or "").strip() else None
                except ValueError:v=None
                if v is not None and not 0<=v<=100:v=None
                item[sub]=v
                if v is not None:marks.append(v)
            item["_average"]=sum(marks)/len(marks) if marks else None; rows.append(item)
    return rows,subjects
def export(rows,subjects,out):
    with open(out/"cleaned_marks.csv","w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=["enrollment","name"]+subjects); w.writeheader()
        for r in rows:w.writerow({k:"" if r[k] is None else r[k] for k in w.fieldnames})
    with open(out/"summary.csv","w",newline="",encoding="utf-8") as f:
        fields=["subject","count","minimum","maximum","average"]; w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
        for sub in subjects:
            vals=[r[sub] for r in rows if r[sub] is not None]
            w.writerow({"subject":sub,"count":len(vals),"minimum":min(vals) if vals else "","maximum":max(vals) if vals else "","average":sum(vals)/len(vals) if vals else ""})
def charts(rows,subjects,out):
    marks=[r[s] for r in rows for s in subjects if r[s] is not None]
    bands={"A (90-100)":0,"B (75-89.99)":0,"C (60-74.99)":0,"D (40-59.99)":0,"F (<40)":0}
    for x in marks:
        bands["A (90-100)" if x>=90 else "B (75-89.99)" if x>=75 else "C (60-74.99)" if x>=60 else "D (40-59.99)" if x>=40 else "F (<40)"]+=1
    plt.figure(figsize=(8,5)); plt.bar(list(bands),list(bands.values())); plt.xticks(rotation=20,ha="right"); plt.title("Grade Distribution"); plt.tight_layout(); plt.savefig(out/"grade_distribution.png"); plt.close()
    avgs=[sum(r[s] for r in rows if r[s] is not None)/max(1,sum(r[s] is not None for r in rows)) for s in subjects]
    plt.figure(figsize=(8,5)); plt.bar(subjects,avgs); plt.title("Subject-wise Average"); plt.tight_layout(); plt.savefig(out/"subject_average.png"); plt.close()
    top=sorted((r for r in rows if r["_average"] is not None),key=lambda r:(-r["_average"],r["name"].casefold()))[:10]
    plt.figure(figsize=(8,5)); plt.bar([r["name"] for r in top],[r["_average"] for r in top]); plt.xticks(rotation=30,ha="right"); plt.title("Top Performers"); plt.tight_layout(); plt.savefig(out/"top_performers.png"); plt.close()
def main():
    if len(sys.argv)!=3:raise SystemExit("Usage: python 12402080601160_Assignment2_Q10.py marks.csv output_folder")
    try:
        out=Path(sys.argv[2]); out.mkdir(parents=True,exist_ok=True); rows,subjects=load(sys.argv[1]); export(rows,subjects,out); charts(rows,subjects,out)
        print("Created cleaned_marks.csv, summary.csv and three chart PNG files.")
    except (OSError,ValueError) as e:raise SystemExit(f"Error: {e}")
if __name__=="__main__":main()
