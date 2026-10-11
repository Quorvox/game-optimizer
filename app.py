"""мин гуи, выбор игры и кнопки"""
import tkinter as tk
from tkinter import ttk, messagebox
from optimizer import load_profiles, optimize, restore, set_prio

# загр профили
profiles = load_profiles()
saved_scheme = {"guid": None}


# лог в текст
def log(msg):
    txt.insert("end", msg + "\n")
    txt.see("end")


# кноп оптимиз
def on_opt():
    key = combo.get()
    if key not in profiles:
        messagebox.showwarning("игра", "выбери игру из списка")
        return
    try:
        rep = optimize(key, profiles)
        saved_scheme["guid"] = rep["old_scheme"]
        log(f"игра: {rep['game']}")
        log(f"старая схема: {rep['old_scheme']}")
        log(f"убито: {len(rep['killed'])} -> {', '.join(rep['killed']) or 'пусто'}")
        # проб поднять приоритет если игра уже запущ
        p = profiles[key]["process"]
        ok = set_prio(p, profiles[key].get("priority", "high"))
        log(f"приоритет {p}: {'ок' if ok else 'проц не найден, запусти игру'}")
    except Exception as e:
        messagebox.showerror("ошиб", str(e))


# кноп откат
def on_back():
    if not saved_scheme["guid"]:
        messagebox.showinfo("откат", "нечего откат, сначала оптимиз")
        return
    try:
        restore(saved_scheme["guid"])
        log(f"вернул схему: {saved_scheme['guid']}")
    except Exception as e:
        messagebox.showerror("ошиб", str(e))


root = tk.Tk()
root.title("game optimizer")
root.geometry("460x360")

ttk.Label(root, text="выбери игру:").pack(pady=6)
combo = ttk.Combobox(root, values=list(profiles.keys()), state="readonly")
combo.set("cs2")
combo.pack()

frm = ttk.Frame(root)
frm.pack(pady=8)
ttk.Button(frm, text="оптимизировать", command=on_opt).pack(side="left", padx=5)
ttk.Button(frm, text="откатить", command=on_back).pack(side="left", padx=5)

txt = tk.Text(root, height=12)
txt.pack(fill="both", expand=True, padx=8, pady=8)

root.mainloop()
