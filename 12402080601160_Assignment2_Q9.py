"""Q9 Inventory classes with merge (+) and total-value comparison (<). Input JSON."""
import json,sys
from dataclasses import dataclass
@dataclass
class Product:
    product_id:str; name:str; stock:int; purchase:float; selling:float
    def __post_init__(self):
        if not self.product_id or not self.name or self.stock<0 or self.purchase<0 or self.selling<0:raise ValueError("Invalid product values")
class Inventory:
    def __init__(self,products=()):
        self.products={}
        for p in products:self.add(p)
    def add(self,p):
        if p.product_id in self.products:raise ValueError(f"Duplicate product ID: {p.product_id}")
        self.products[p.product_id]=p
    def delete(self,pid):
        if pid not in self.products:raise KeyError(pid)
        del self.products[pid]
    def update(self,pid,stock):
        if pid not in self.products:raise KeyError(pid)
        if stock<0:raise ValueError("Stock cannot be negative")
        self.products[pid].stock=stock
    def total_value(self):return sum(p.stock*p.purchase for p in self.products.values())
    def __lt__(self,other):return self.total_value()<other.total_value()
    def __add__(self,other):
        result=Inventory(Product(**vars(p)) for p in self.products.values())
        for p in other.products.values():
            if p.product_id not in result.products:result.add(Product(**vars(p)))
            else:
                old=result.products[p.product_id]
                if old.name!=p.name:raise ValueError(f"Conflicting product names for {p.product_id}")
                old.stock+=p.stock; old.purchase=min(old.purchase,p.purchase); old.selling=max(old.selling,p.selling)
        return result
    def display(self):
        for pid in sorted(self.products):
            p=self.products[pid]; print(f"{pid} {p.name} stock={p.stock} purchase={p.purchase:g} selling={p.selling:g}")
        print(f"TOTAL_VALUE {self.total_value():g}")
def make(rows):return Inventory(Product(str(x["id"]),str(x["name"]),int(x["stock"]),float(x["purchase"]),float(x["selling"])) for x in rows)
def main():
    try:
        data=json.load(sys.stdin); a=make(data.get("inventory_a",[])); b=make(data.get("inventory_b",[])); merged=a+b
        print("MERGED"); merged.display(); print("COMPARE","A<B" if a<b else "A>=B")
    except (ValueError,KeyError,TypeError,json.JSONDecodeError) as e:raise SystemExit(f"Input error: {e}")
if __name__=="__main__":main()
