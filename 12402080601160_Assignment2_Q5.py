"""Q5 Tkinter Contact Manager with MySQL. pip install mysql-connector-python."""
import os, re, tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error
EMAIL=re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
class ContactManager(tk.Tk):
    def __init__(self):
        super().__init__(); self.title("Contact Manager"); self.geometry("900x570")
        self.db=mysql.connector.connect(host=os.getenv("MYSQL_HOST","localhost"),user=os.getenv("MYSQL_USER","root"),password=os.getenv("MYSQL_PASSWORD",""),database=os.getenv("MYSQL_DATABASE","assignment2"))
        cur=self.db.cursor(); cur.execute("""CREATE TABLE IF NOT EXISTS Contact(id INT AUTO_INCREMENT PRIMARY KEY,name VARCHAR(100) NOT NULL,email VARCHAR(150) NOT NULL UNIQUE,phone VARCHAR(25) NOT NULL,category VARCHAR(40) NOT NULL,notes TEXT)"""); self.db.commit(); cur.close()
        self.name=tk.StringVar(); self.email=tk.StringVar(); self.phone=tk.StringVar(); self.category=tk.StringVar(value="Personal"); self.search=tk.StringVar()
        form=ttk.LabelFrame(self,text="Contact details",padding=8); form.pack(fill="x",padx=10,pady=8)
        for i,label in enumerate(("Name","Email","Phone","Category")): ttk.Label(form,text=label).grid(row=0,column=i,sticky="w",padx=4)
        ttk.Entry(form,textvariable=self.name,width=20).grid(row=1,column=0,padx=4)
        ttk.Entry(form,textvariable=self.email,width=25).grid(row=1,column=1,padx=4)
        ttk.Entry(form,textvariable=self.phone,width=16).grid(row=1,column=2,padx=4)
        ttk.Combobox(form,textvariable=self.category,values=["Personal","Faculty","Work","Other"],state="readonly",width=12).grid(row=1,column=3,padx=4)
        ttk.Label(form,text="Notes").grid(row=2,column=0,sticky="w"); self.notes=tk.Text(form,height=3,width=75); self.notes.grid(row=3,column=0,columnspan=4,pady=4)
        for label,cmd in [("Add",self.add),("Update",self.update),("Delete",self.delete),("Clear",self.clear)] : ttk.Button(form,text=label,command=cmd).grid(row=4,column=[("Add",self.add),("Update",self.update),("Delete",self.delete),("Clear",self.clear)].index((label,cmd)),pady=5)
        bar=ttk.Frame(self); bar.pack(fill="x",padx=10); ttk.Entry(bar,textvariable=self.search,width=35).pack(side="left"); ttk.Button(bar,text="Search",command=self.search_rows).pack(side="left",padx=4); ttk.Button(bar,text="Show all",command=self.refresh).pack(side="left")
        self.table=ttk.Treeview(self,columns=("id","name","email","phone","category","notes"),show="headings")
        for c,w in zip(("id","name","email","phone","category","notes"),(45,130,180,110,90,250)): self.table.heading(c,text=c.title()); self.table.column(c,width=w)
        self.table.pack(fill="both",expand=True,padx=10,pady=10); self.table.bind("<<TreeviewSelect>>",self.load); self.refresh()
    def values(self):
        v=(self.name.get().strip(),self.email.get().strip(),self.phone.get().strip(),self.category.get(),self.notes.get("1.0","end").strip())
        if not all(v[:3]): raise ValueError("Name, email and phone are required.")
        if not EMAIL.fullmatch(v[1]): raise ValueError("Enter a valid email.")
        return v
    def add(self):
        try:
            cur=self.db.cursor(); cur.execute("INSERT INTO Contact(name,email,phone,category,notes) VALUES(%s,%s,%s,%s,%s)",self.values()); self.db.commit(); cur.close(); self.refresh(); self.clear()
        except (ValueError,Error) as e: messagebox.showerror("Add contact",str(e))
    def selected(self):
        s=self.table.selection()
        if not s: raise ValueError("Select a contact first.")
        return int(self.table.item(s[0],"values")[0])
    def update(self):
        try:
            cid=self.selected(); v=self.values(); cur=self.db.cursor(); cur.execute("UPDATE Contact SET name=%s,email=%s,phone=%s,category=%s,notes=%s WHERE id=%s",v+(cid,)); self.db.commit(); cur.close(); self.refresh()
        except (ValueError,Error) as e: messagebox.showerror("Update contact",str(e))
    def delete(self):
        try:
            cid=self.selected()
            if not messagebox.askyesno("Confirm","Delete selected contact?"): return
            cur=self.db.cursor(); cur.execute("DELETE FROM Contact WHERE id=%s",(cid,)); self.db.commit(); cur.close(); self.refresh(); self.clear()
        except (ValueError,Error) as e: messagebox.showerror("Delete contact",str(e))
    def rows(self,sql,params=()):
        cur=self.db.cursor(); cur.execute(sql,params); data=cur.fetchall(); cur.close()
        for item in self.table.get_children(): self.table.delete(item)
        for row in data: self.table.insert("","end",values=tuple("" if x is None else x for x in row))
    def refresh(self): self.rows("SELECT id,name,email,phone,category,notes FROM Contact ORDER BY name")
    def search_rows(self):
        term="%"+self.search.get().strip()+"%"; self.rows("SELECT id,name,email,phone,category,notes FROM Contact WHERE name LIKE %s OR email LIKE %s OR phone LIKE %s ORDER BY name",(term,term,term))
    def load(self,_=None):
        s=self.table.selection()
        if not s:return
        v=self.table.item(s[0],"values"); self.clear(); self.name.set(v[1]); self.email.set(v[2]); self.phone.set(v[3]); self.category.set(v[4]); self.notes.insert("1.0",v[5])
    def clear(self):
        self.name.set(""); self.email.set(""); self.phone.set(""); self.category.set("Personal"); self.notes.delete("1.0","end")
    def close(self):
        self.db.close(); self.destroy()
def main():
    try:
        app=ContactManager(); app.protocol("WM_DELETE_WINDOW",app.close); app.mainloop()
    except Error as e: messagebox.showerror("Database connection",str(e))
if __name__=="__main__": main()
