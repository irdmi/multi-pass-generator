import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import secrets
import string
import os
from datetime import datetime
from PIL import Image, ImageTk
import sys

def get_resource_path(relative_path):
    """Получить абсолютный путь к ресурсу (работает и в скрипте, и в EXE)"""
    if getattr(sys, 'frozen', False):
        # Запущен как EXE — ресурсы в _MEIPASS
        base_path = sys._MEIPASS
    else:
        # Запущен как скрипт — текущая директория
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

LANG = {
    "ru": {
        "title": "Генератор надёжных ключей", 
        "theme_light": "Светлая тема", 
        "theme_dark": "Тёмная тема",
        "lang_btn": "EN", 
        "blocks_title": "Блоки ключей", 
        "add_block": "Добавить блок",
        "generate": "Сгенерировать", 
        "open_explorer": "Открыть папку",
        "count_lbl": "Количество:", 
        "length_lbl": "Длина:", 
        "sym_title": "Наборы символов",
        "lower": "Строчные лат. (a–z)", 
        "upper": "Заглавные лат. (A–Z)",
        "digits": "Цифры (0–9)", 
        "symbols": "Спецсимволы (!@#$...)",
        "cyr_lower": "Строчные кирилл. (абв...)", 
        "cyr_upper": "Заглавные кирилл. (АБВ...)",
        "arm_lower": "Строчные арм. (աբգ...)", 
        "arm_upper": "Заглавные арм. (ԱԲԳ...)",
        "numbering": "Нумерация в файлах", 
        "name_lbl": "Название:", 
        "desc_lbl": "Описание:",
        "err_count": "Количество > 0", 
        "err_len": "Длина >= 1", 
        "err_chars": "Выберите набор символов",
        "success": "Готово!", 
        "warn_dir": "Сначала сгенерируйте ключи", 
        "select_dir": "Выберите папку"
    },
    "en": {
        "title": "Secure Key Generator", 
        "theme_light": "Light Theme", 
        "theme_dark": "Dark Theme",
        "lang_btn": "RU", 
        "blocks_title": "Key Blocks", 
        "add_block": "Add Block",
        "generate": "Generate", 
        "open_explorer": "Open Folder",
        "count_lbl": "Count:", 
        "length_lbl": "Length:", 
        "sym_title": "Character Sets",
        "lower": "Lowercase Latin (a–z)", 
        "upper": "Uppercase Latin (A–Z)",
        "digits": "Digits (0–9)", 
        "symbols": "Symbols (!@#$...)",
        "cyr_lower": "Lowercase Cyrillic (абв...)", 
        "cyr_upper": "Uppercase Cyrillic (АБВ...)",
        "arm_lower": "Lowercase Armenian (աբգ...)", 
        "arm_upper": "Uppercase Armenian (ԱԲԳ...)",
        "numbering": "Number passwords in files", 
        "name_lbl": "Name:", 
        "desc_lbl": "Description:",
        "err_count": "Count must be > 0", 
        "err_len": "Length must be >= 1", 
        "err_chars": "Select at least one set",
        "success": "Done!", 
        "warn_dir": "Generate keys first", 
        "select_dir": "Select output directory"
    }
}

CHAR_SETS = {
    "lower": string.ascii_lowercase, 
    "upper": string.ascii_uppercase,
    "digits": string.digits, 
    "symbols": '!@#$%^&*()-_=+[]{};:,.<>/?',
    "cyr_lower": 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя',
    "cyr_upper": 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ',
    "arm_lower": 'աբգդեզէըթժիլխծկհձղճմյնշոչպջռսվտրցւփքօֆ',
    "arm_upper": 'ԱԲԳԵԶԷԸԹԺԻԼԽԾԿՀՁՂՃՄՅՆՇՈՉՊՋՌՍՎՏՐՑՒՓՔՕՖ'
}

def generate_password(length, opts):
    pool, req = [], []
    for key, chars in CHAR_SETS.items():
        if opts.get(key):
            pool.extend(chars)
            req.append(secrets.choice(chars))
    if not pool: 
        return None
    rem = max(length - len(req), 0)
    res = [secrets.choice(pool) for _ in range(rem)] + req
    for i in range(len(res)-1, 0, -1):
        j = secrets.randbelow(i+1)
        res[i], res[j] = res[j], res[i]
    return ''.join(res[:length])

class App:
    def __init__(self, root):
        self.root = root
        self.lang = "ru"
        self.dark = False
        self.blocks = []
        self.logo_image = None
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self._trans = []
        self._build_ui()
        self._apply_theme()
        self._load_logo()

    def _t(self, k): 
        return LANG[self.lang][k]

    def _load_logo(self):
        """Загрузка логотипа в иконку окна"""
        try:
            logo_path = get_resource_path("logo.png")
            if os.path.exists(logo_path):
                img = Image.open(logo_path)
                img = img.resize((32, 32), Image.Resampling.LANCZOS)
                self.logo_image = ImageTk.PhotoImage(img)
                self.root.iconphoto(True, self.logo_image)
                print(f"✅ Логотип загружен: {logo_path}")
            else:
                print(f"⚠️ Логотип не найден: {logo_path}")
        except Exception as e:
            print(f"❌ Ошибка загрузки лого: {e}")

    def _build_ui(self):
        self.root.title(self._t("title"))
        self.root.geometry("800x600")
        self.root.minsize(750, 550)
        
        main = ttk.Frame(self.root, padding=15)
        main.pack(fill="both", expand=True)

        tb = ttk.Frame(main)
        tb.pack(fill="x", pady=(0, 10))
        
        ttk.Label(tb, text="").pack(side="left", expand=True, fill="x")
        
        btn_frame = ttk.Frame(tb)
        btn_frame.pack(side="right")
        
        self.lang_btn = ttk.Button(btn_frame, text=self._t("lang_btn"), 
                                  command=self._toggle_lang, width=8)
        self.lang_btn.pack(side="right", padx=(5, 0))
        
        self.theme_btn = ttk.Button(btn_frame, text=self._t("theme_dark"), 
                                   command=self._toggle_theme, width=12)
        self.theme_btn.pack(side="right")

        header_frame = ttk.Frame(main)
        header_frame.pack(fill="x", pady=(5, 5))
        
        blocks_title_lbl = ttk.Label(header_frame, text=self._t("blocks_title"), 
                                    font=("Segoe UI", 11, "bold"))
        blocks_title_lbl.pack(side="left")
        self._trans.append((blocks_title_lbl, "blocks_title"))

        self.blocks_fr = ttk.LabelFrame(main, text="", padding=10)
        self.blocks_fr.pack(fill="both", expand=True, pady=(0, 10))

        canvas = tk.Canvas(self.blocks_fr, highlightthickness=0)
        sb = ttk.Scrollbar(self.blocks_fr, orient="vertical", command=canvas.yview)
        self.inner = ttk.Frame(canvas)
        
        self.inner.bind("<Configure>", 
                       lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.inner, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        
        canvas.bind_all("<MouseWheel>", 
                       lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        self.add_block()

        act = ttk.Frame(main)
        act.pack(fill="x", pady=(10, 0))
        
        add_btn = ttk.Button(act, text=self._t("add_block"), 
                            command=self.add_block, width=18)
        add_btn.pack(side="left", padx=(0, 10))
        self._trans.append((add_btn, "add_block"))
        
        gen_btn = ttk.Button(act, text=self._t("generate"), 
                            command=self.generate, width=18)
        gen_btn.pack(side="left", padx=(0, 10))
        self._trans.append((gen_btn, "generate"))
        
        open_btn = ttk.Button(act, text=self._t("open_explorer"), 
                             command=self.open_dir, width=18)
        open_btn.pack(side="left")
        self._trans.append((open_btn, "open_explorer"))
        
        self.style.configure("Accent.TButton", font=("Segoe UI", 9, "bold"))
        self.style.configure("Exp.TButton", font=("Segoe UI", 9, "bold"))

    def _toggle_theme(self):
        self.dark = not self.dark
        self._apply_theme()
        self.theme_btn.config(text=self._t("theme_light" if self.dark else "theme_dark"))

    def _apply_theme(self):
        if self.dark:
            bg, fg, eb, acc, exp = "#2b2b2b", "#ffffff", "#3c3c3c", "#0078d7", "#28a745"
            btn_bg, btn_fg = "#404040", "#ffffff"
        else:
            bg, fg, eb, acc, exp = "#f0f0f0", "#000000", "#ffffff", "#007ACC", "#28a745"
            btn_bg, btn_fg = "#e1e1e1", "#000000"
        
        self.root.config(bg=bg)
        
        self.style.configure("TFrame", background=bg)
        self.style.configure("TLabelframe", background=bg, foreground=fg, 
                           lightcolor=bg, darkcolor=bg)
        self.style.configure("TLabelframe.Label", background=bg, foreground=fg,
                           font=("Segoe UI", 10, "bold"))
        self.style.configure("TLabel", background=bg, foreground=fg)
        self.style.configure("TButton", background=btn_bg, foreground=btn_fg,
                           bordercolor=btn_bg, darkcolor=btn_bg, lightcolor=btn_bg,
                           font=("Segoe UI", 9))
        self.style.configure("TEntry", fieldbackground=eb, foreground=fg,
                           bordercolor="#999" if not self.dark else "#555",
                           lightcolor=eb, darkcolor=eb)
        self.style.configure("TCheckbutton", background=bg, foreground=fg,
                           indicatorbackground=eb if not self.dark else "#555",
                           indicatorforeground=fg)
        self.style.configure("TScrollbar", background=bg, 
                           troughcolor="#404040" if self.dark else "#d1d1d1",
                           arrowcolor=fg)
        self.style.configure("Accent.TButton", background=acc, foreground="white",
                           bordercolor=acc, darkcolor=acc, lightcolor=acc)
        self.style.configure("Exp.TButton", background=exp, foreground="white",
                           bordercolor=exp, darkcolor=exp, lightcolor=exp)
        
        self.style.map("TButton",
                      background=[("active", "#005a9e" if not self.dark else "#005a9e"),
                                 ("pressed", "#004578"),
                                 ("!active", btn_bg)],
                      foreground=[("active", "white"),
                                 ("pressed", "white"),
                                 ("!active", btn_fg)])
        
        self.style.map("Accent.TButton",
                      background=[("active", "#005a9e"), ("pressed", "#004578")],
                      foreground=[("active", "white"), ("pressed", "white")])
        
        self.style.map("Exp.TButton",
                      background=[("active", "#218838"), ("pressed", "#1e7e34")],
                      foreground=[("active", "white"), ("pressed", "white")])
        
        for child in self.root.winfo_children():
            self._color_rec(child, bg, fg, eb)
        
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Canvas):
                        child.config(bg=bg, highlightthickness=0)
        
        self.root.update_idletasks()

    def _color_rec(self, w, bg, fg, eb):
        try:
            if isinstance(w, (tk.Frame, ttk.Frame)):
                w.config(style="TFrame")
            elif isinstance(w, (tk.LabelFrame, ttk.LabelFrame)):
                w.config(style="TLabelframe")
            elif isinstance(w, (tk.Label, ttk.Label)):
                w.config(background=bg, foreground=fg)
            elif isinstance(w, tk.Entry):
                w.config(bg=eb, fg=fg, insertcolor=fg, 
                        highlightbackground="#999" if not self.dark else "#555")
            elif isinstance(w, tk.Canvas):
                w.config(bg=bg, highlightthickness=0)
            elif isinstance(w, tk.Checkbutton):
                w.config(bg=bg, fg=fg, activebackground=bg, 
                        activeforeground=fg, selectcolor=bg)
        except Exception:
            pass
        
        for c in w.winfo_children():
            self._color_rec(c, bg, fg, eb)

    def _toggle_lang(self):
        self.lang = "en" if self.lang == "ru" else "ru"
        self.root.title(self._t("title"))
        
        for w, key in self._trans:
            try:
                w.config(text=self._t(key))
            except:
                pass
        
        for b in self.blocks:
            try:
                b["name_lbl"].config(text=self._t("name_lbl"))
                b["desc_lbl"].config(text=self._t("desc_lbl"))
                b["count_lbl"].config(text=self._t("count_lbl"))
                b["len_lbl"].config(text=self._t("length_lbl"))
                b["sym_fr"].config(text=self._t("sym_title"))
                b["num_chk"].config(text=self._t("numbering"))
                
                for chk, k in b["checks"]:
                    chk.config(text=self._t(k))
            except:
                pass

    def add_block(self):
        idx = len(self.blocks) + 1
        fr = ttk.LabelFrame(self.inner, text=f"Блок {idx}", padding=10)
        fr.pack(fill="x", pady=8, padx=5)

        name_v, desc_v = tk.StringVar(value=f"Блок {idx}"), tk.StringVar()
        
        info_fr = ttk.Frame(fr)
        info_fr.pack(fill="x", pady=(0, 8))
        
        name_lbl = ttk.Label(info_fr, text=self._t("name_lbl"))
        name_lbl.pack(side="left", padx=(0, 5))
        name_ent = ttk.Entry(info_fr, textvariable=name_v, width=20)
        name_ent.pack(side="left", padx=(0, 15))
        
        desc_lbl = ttk.Label(info_fr, text=self._t("desc_lbl"))
        desc_lbl.pack(side="left", padx=(0, 5))
        desc_ent = ttk.Entry(info_fr, textvariable=desc_v, width=25)
        desc_ent.pack(side="left")

        params_fr = ttk.Frame(fr)
        params_fr.pack(fill="x", pady=(0, 8))
        
        count_lbl = ttk.Label(params_fr, text=self._t("count_lbl"))
        count_lbl.pack(side="left", padx=(0, 5))
        count_v = tk.IntVar(value=10)
        count_ent = ttk.Entry(params_fr, textvariable=count_v, width=8)
        count_ent.pack(side="left", padx=(0, 20))
        
        len_lbl = ttk.Label(params_fr, text=self._t("length_lbl"))
        len_lbl.pack(side="left", padx=(0, 5))
        len_v = tk.IntVar(value=16)
        len_ent = ttk.Entry(params_fr, textvariable=len_v, width=8)
        len_ent.pack(side="left")

        sym_fr = ttk.LabelFrame(fr, text=self._t("sym_title"), padding=8)
        sym_fr.pack(fill="x", pady=(0, 8))
        
        opts = [("lower", True), ("upper", True), ("digits", True), ("symbols", True),
                ("cyr_lower", False), ("cyr_upper", False), 
                ("arm_lower", False), ("arm_upper", False)]
        checks, vars_ = [], []
        
        for i, (k, def_v) in enumerate(opts):
            v = tk.BooleanVar(value=def_v)
            chk = ttk.Checkbutton(sym_fr, text=self._t(k), variable=v)
            chk.grid(row=i//2, column=i%2, sticky="w", padx=10, pady=3)
            checks.append((chk, k))
            vars_.append(v)

        num_v = tk.BooleanVar(value=True)
        num_chk = ttk.Checkbutton(fr, text=self._t("numbering"), variable=num_v)
        num_chk.pack(anchor="w", pady=(5, 0))

        self.blocks.append({
            "frame": fr, "name_v": name_v, "desc_v": desc_v, 
            "count_v": count_v, "len_v": len_v,
            "vars": vars_, "checks": checks, "num_v": num_v,
            "name_lbl": name_lbl, "desc_lbl": desc_lbl,
            "count_lbl": count_lbl, "len_lbl": len_lbl, 
            "sym_fr": sym_fr, "num_chk": num_chk
        })
        
        self.inner.update_idletasks()

    def generate(self):
        out = filedialog.askdirectory(title=self._t("select_dir"))
        if not out: 
            return
        
        base = os.path.join(out, "generated_keys")
        os.makedirs(base, exist_ok=True)

        readme = os.path.join(base, "README.txt")
        with open(readme, "w", encoding="utf-8") as f:
            f.write(f"Date: {datetime.now():%Y-%m-%d %H:%M:%S}\n\n")
            
            for i, b in enumerate(self.blocks):
                if not any(v.get() for v in b["vars"]):
                    messagebox.showerror("Error", 
                                       f"{self._t('err_chars')} (#{i+1})")
                    return
                    
                name, desc = b["name_v"].get().strip(), b["desc_v"].get().strip()
                count, length = b["count_v"].get(), b["len_v"].get()
                
                if count <= 0: 
                    messagebox.showerror("Error", 
                                       f"{self._t('err_count')} (#{i+1})")
                    return
                if length < 1: 
                    messagebox.showerror("Error", 
                                       f"{self._t('err_len')} (#{i+1})")
                    return

                opts = {k: v.get() for k, v in zip(
                    ("lower","upper","digits","symbols",
                     "cyr_lower","cyr_upper","arm_lower","arm_upper"), 
                    b["vars"])}
                
                pws = [generate_password(length, opts) for _ in range(count)]
                
                dir_name = f"block_{i+1}_{name.replace(' ', '_')}"
                dir_path = os.path.join(base, dir_name)
                os.makedirs(dir_path, exist_ok=True)

                # Создаём ОБА файла: с нумерацией и без
                # Файл БЕЗ нумерации
                with open(os.path.join(dir_path, "keys.txt"), "w", 
                         encoding="utf-8") as fw:
                    for p in pws:
                        fw.write(f"{p}\n")
                
                # Файл С нумерацией
                with open(os.path.join(dir_path, "keys_numbered.txt"), "w", 
                         encoding="utf-8") as fw:
                    for idx, p in enumerate(pws, 1):
                        fw.write(f"{idx}. {p}\n")
                        
                f.write(f"[{dir_name}] Count: {count}, Len: {length}, "
                       f"Desc: {desc or '—'}\n")
                f.write(f"  Files: keys.txt (no numbering), keys_numbered.txt (with numbering)\n\n")

        self.last_dir = base
        messagebox.showinfo("OK", self._t("success"))

    def open_dir(self):
        if hasattr(self, "last_dir") and os.path.exists(self.last_dir):
            if os.name == "nt":
                os.startfile(self.last_dir)
            elif os.name == "posix":
                os.system(f"open {self.last_dir}")
            else:
                os.system(f"xdg-open {self.last_dir}")
        else:
            messagebox.showwarning("Warn", self._t("warn_dir"))

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()