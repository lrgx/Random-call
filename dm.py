import random
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import scrolledtext, messagebox

# ================= 数据 =================
names = []
rolling = False
current_theme = "morph"

# ================= 文件操作 =================
def load_names():
    try:
        with open("name.txt", "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
            names.clear()
            for line in lines:
                names.extend(line.split())
        update_textbox()
        messagebox.showinfo("成功", "名字列表加载成功")
    except FileNotFoundError:
        if messagebox.askyesno("提示", "找不到 name.txt，是否创建？"):
            open("name.txt", "w", encoding="utf-8").close()
    except Exception as e:
        messagebox.showerror("错误", str(e))


def save_names():
    try:
        text = text_area.get(1.0, END).strip()
        names.clear()
        for line in text.splitlines():
            names.extend(line.split())
        with open("name.txt", "w", encoding="utf-8") as f:
            f.write(text)
        messagebox.showinfo("成功", "保存成功")
    except Exception as e:
        messagebox.showerror("错误", str(e))


# ================= 逻辑 =================
def update_textbox():
    text_area.delete(1.0, END)
    for i in range(0, len(names), 10):
        text_area.insert(END, " ".join(names[i:i + 10]) + "\n")


def count_names():
    name_label.config(text=f"名字数量：{len(names)}")


# ================= 🎲 滚动动画 =================
def generate_name():
    global rolling
    if not names:
        messagebox.showwarning("提示", "名字列表为空")
        count_names()
        return
    if rolling:
        return

    rolling = True
    roll_step(0, 40)


def roll_step(step, max_step):
    global rolling
    name_label.config(text=random.choice(names))

    if step < max_step:
        delay = 30 + step * 3
        window.after(delay, roll_step, step + 1, max_step)
    else:
        rolling = False


def toggle_theme():
    global current_theme
    current_theme = "darkly" if current_theme == "morph" else "morph"
    window.style.theme_use(current_theme)
    theme_btn.config(
        text="浅色模式" if current_theme == "darkly" else "深色模式"
    )


# ================= UI =================
window = ttk.Window(
    title="随机名字生成器",
    themename=current_theme,
    size=(1000, 300),
    resizable=(False, False)
)

# ---------- 结果区 ----------
result_frame = ttk.LabelFrame(window, text="随机结果")
result_frame.pack(fill=X, padx=20, pady=(15, 10))

result_inner = ttk.Frame(result_frame, padding=15)
result_inner.pack(fill=BOTH, expand=True)

name_label = ttk.Label(
    result_inner,
    text="",
    font=("微软雅黑", 30, "bold"),
    bootstyle="inverse"
)
name_label.pack(pady=10)

# ---------- 按钮区 ----------
button_frame = ttk.Frame(window)
button_frame.pack(pady=10)

ttk.Button(
    button_frame, text="开始抽取",
    command=generate_name,
    width=16,
    bootstyle=DEFAULT
).pack(side=LEFT, padx=6)

ttk.Button(
    button_frame, text="数量",
    command=count_names,
    width=10,
    bootstyle=DEFAULT
).pack(side=LEFT, padx=6)

ttk.Button(
    button_frame, text="加载",
    command=load_names,
    width=10,
    bootstyle=DEFAULT
).pack(side=LEFT, padx=6)

ttk.Button(
    button_frame, text="保存",
    command=save_names,
    width=10,
    bootstyle=DEFAULT
).pack(side=LEFT, padx=6)

theme_btn = ttk.Button(
    button_frame,
    text="深色模式",
    command=toggle_theme,
    width=12,
    bootstyle=DEFAULT
)
theme_btn.pack(side=LEFT, padx=6)

# ---------- 编辑区 ----------
edit_visible = ttk.BooleanVar(value=False)

def toggle_edit():
    if edit_visible.get():
        edit_frame.pack_forget()
        toggle_edit_btn.config(text="显示编辑")
        window.geometry("1000x300")
    else:
        edit_frame.pack(fill=BOTH, expand=True, padx=20, pady=(5, 15))
        toggle_edit_btn.config(text="隐藏编辑")
        window.geometry("1000x600")
    edit_visible.set(not edit_visible.get())


toggle_edit_btn = ttk.Button(
    button_frame,
    text="显示编辑",
    command=toggle_edit,
    width=12,
    bootstyle=DEFAULT
)
toggle_edit_btn.pack(side=LEFT, padx=6)

edit_frame = ttk.LabelFrame(window, text="名字列表编辑")

edit_inner = ttk.Frame(edit_frame, padding=10)
edit_inner.pack(fill=BOTH, expand=True)

text_area = scrolledtext.ScrolledText(
    edit_inner,
    height=15,
    font=("微软雅黑", 12)
)
text_area.pack(fill=BOTH, expand=True)

status_frame = ttk.Frame(window)
status_frame.pack(side=BOTTOM, fill=X)

ttk.Label(
    status_frame,
    text="就绪",
    anchor=W,
    font=("微软雅黑", 9)
).pack(side=LEFT, padx=10)

ttk.Label(
    status_frame,
    text="by lrgx & Aaron",
    anchor=E,
    font=("微软雅黑", 9)
).pack(side=RIGHT, padx=10)
# ================= 启动 =================
load_names()
window.mainloop()