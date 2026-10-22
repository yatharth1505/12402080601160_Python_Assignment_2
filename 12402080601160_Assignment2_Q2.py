"""Q2 Offline HTML product ranker. Input: p k, then HTML paths."""
import re, sys
from html.parser import HTMLParser

class Parser(HTMLParser):
    def __init__(self):
        super().__init__(); self.items=[]; self.current=None; self.field=None; self.depth=0
    def handle_starttag(self, tag, attrs):
        c=set(dict(attrs).get("class","").lower().split())
        if c & {"product","product-card"}:
            if self.current: self.items.append(self.current)
            self.current={"name":"","price":"","rating":""}
        if self.current:
            for classes, field in [({"product-name","name","title"},"name"),({"price","product-price"},"price"),({"rating","product-rating"},"rating")]:
                if c & classes: self.field=field; self.depth=1; return
            if self.field: self.depth += 1
    def handle_endtag(self, tag):
        if self.field:
            self.depth -= 1
            if self.depth <= 0: self.field=None; self.depth=0
    def handle_data(self, data):
        if self.current and self.field: self.current[self.field] += data.strip()
    def close(self):
        super().close()
        if self.current: self.items.append(self.current); self.current=None

def number(raw):
    match=re.search(r"\d+(?:\.\d+)?", raw or "")
    return float(match.group()) if match else None

def read_page(path):
    parser=Parser()
    with open(path, encoding="utf-8", errors="replace") as f: parser.feed(f.read())
    result=[]
    for p in parser.items:
        price=number(p["price"].replace(",","")); rating=number(p["rating"]); name=" ".join(p["name"].split())
        if name and price is not None and rating is not None and 0 <= rating <= 5:
            result.append({"name":name,"price":price,"rating":rating})
    return result

def main():
    lines=[x.strip() for x in sys.stdin if x.strip()]
    try:
        p,k=map(int,lines[0].split()); paths=lines[1:1+p]
        if p<1 or k<1 or len(paths)!=p: raise ValueError("Expected p k and p file paths.")
        unique={}
        for path in paths:
            for item in read_page(path):
                key=item["name"].casefold(); old=unique.get(key)
                if old is None or (-item["rating"],item["price"],item["name"]) < (-old["rating"],old["price"],old["name"]): unique[key]=item
        ranked=sorted(unique.values(),key=lambda x:(-x["rating"],x["price"],x["name"].casefold()))
        for x in ranked[:k]:
            price=int(x["price"]) if x["price"].is_integer() else x["price"]
            print(x["name"],price,f'{x["rating"]:.1f}')
    except (ValueError,IndexError,OSError) as e: raise SystemExit(f"Input/file error: {e}")
if __name__=="__main__": main()
