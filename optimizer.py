"""кор логика оптимизатора, только винда"""
import json
import re
import subprocess
import psutil

# гуид макс производ
HIGH_PERF = "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"


# пол актив схему питания
def get_scheme():
    out = subprocess.check_output(["powercfg", "/GETACTIVESCHEME"], text=True)
    # ищем гуид регексом, тк локаль разная
    m = re.search(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}", out)
    return m.group(0) if m else ""


# пост схему по гуид
def set_scheme(guid):
    subprocess.check_call(["powercfg", "/SETACTIVE", guid])


# загр профили игр из json
def load_profiles(path="profiles.json"):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

  
# убить фон из списка, возвр отчет
def kill_bg(kill_list):
    killed = []
    skip = []
    kill_low = {k.lower() for k in kill_list}
    for p in psutil.process_iter(["pid", "name"]):
        try:
            name = (p.info["name"] or "").lower()
            if name in kill_low:
                p.terminate()
                killed.append(p.info["name"])
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            skip.append(p.info.get("name", "?"))
    return killed, skip


# пост приоритет процессу игры
def set_prio(proc_name, level="high"):
    found = False
    for p in psutil.process_iter(["name"]):
        try:
            if (p.info["name"] or "").lower() == proc_name.lower():
                if level == "high":
                    p.nice(psutil.HIGH_PRIORITY_CLASS)
                else:
                    p.nice(psutil.NORMAL_PRIORITY_CLASS)
                found = True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return found


# гл оптимизация под игру, возвр отчет dict
def optimize(game_key, profiles):
    prof = profiles[game_key]
    old = get_scheme()
    set_scheme(HIGH_PERF)
    killed, skip = kill_bg(prof.get("kill", []))
    return {"old_scheme": old, "killed": killed, "skipped": len(skip), "game": prof["label"]}


# откат схемы назад
def restore(guid):
    set_scheme(guid)
