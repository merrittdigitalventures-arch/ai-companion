import os
import tkinter as tk
from tkinter import messagebox, ttk
from operatoros.api_fetcher import APIFetcher
from operatoros.logger import log_run

class OperatorOSGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("OperatorOS Beta GUI")
        self.fetcher = APIFetcher()
        self.niches = []

        self.create_widgets()
        self.load_niches()

    def create_widgets(self):
        tk.Label(self.root, text="Trending Niches & Revenue", font=("Helvetica", 14)).pack(pady=10)
        
        self.tree = ttk.Treeview(self.root, columns=("Score", "Revenue"), show="headings", height=8)
        self.tree.heading("Score", text="Score")
        self.tree.heading("Revenue", text="Revenue")
        self.tree.column("Score", width=80, anchor="center")
        self.tree.column("Revenue", width=100, anchor="center")
        self.tree.pack(padx=20, pady=10)

        self.select_btn = tk.Button(self.root, text="Select Highlighted Niche", command=self.select_niche)
        self.select_btn.pack(pady=5)

        self.manual_frame = tk.Frame(self.root)
        tk.Label(self.manual_frame, text="Or enter niche manually:").pack(side="left")
        self.manual_entry = tk.Entry(self.manual_frame)
        self.manual_entry.pack(side="left", padx=5)
        self.manual_btn = tk.Button(self.manual_frame, text="Add Niche", command=self.add_manual_niche)
        self.manual_btn.pack(side="left", padx=5)
        self.manual_frame.pack(pady=5)

        self.selected_label = tk.Label(self.root, text="Selected Niche: None", font=("Helvetica", 12, "bold"))
        self.selected_label.pack(pady=10)

    def load_niches(self):
        try:
            trends = self.fetcher.fetch_trends()
            financials = self.fetcher.fetch_financials()
            name_to_rev = {f['name']: f.get('revenue', 0) for f in financials}
            scored = []
            for t in trends:
                name = t['name']
                revenue = name_to_rev.get(name, 0)
                scored.append({"name": name, "score": revenue, "revenue": revenue})
            self.niches = scored
            self.refresh_tree()
            log_run("Niches loaded and scored.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load niches: {e}")
            log_run(f"Niches load error: {e}")

    def refresh_tree(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for niche in self.niches:
            self.tree.insert("", "end", values=(niche["name"], niche["score"], niche["revenue"]))

    def select_niche(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Please select a niche first.")
            return
        item = self.tree.item(selected[0])
        name = item['values'][0]
        self.selected_label.config(text=f"Selected Niche: {name}")
        log_run(f"Niche manually selected: {name}")

    def add_manual_niche(self):
        name = self.manual_entry.get().strip()
        if not name:
            messagebox.showwarning("Empty", "Enter a niche name first.")
            return
        self.niches.append({"name": name, "score": 0, "revenue": 0})
        self.refresh_tree()
        log_run(f"Manual niche added: {name}")
        self.manual_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = OperatorOSGUI(root)
    root.mainloop()
