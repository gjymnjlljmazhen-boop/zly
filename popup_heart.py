"""弹窗爱心 —— 原始 tkinter 版本（保留代码用）。

运行需要带图形界面的桌面环境（Windows / macOS / Linux + X）：
    python3 popup_heart.py
Android 的 proot 里既没有 tkinter 也没有 DISPLAY，跑不起来；
手机上看效果请用同目录的 popup-heart.html。

流程与网页版一一对应：
    1) 100 个 150×60 的置顶小窗沿心形参数方程依次弹出；
    2) 停留 1 秒后全部销毁；
    3) 满屏随机再弹 (屏宽//150)*(屏高//40)+50 个；
    4) 停留 3 秒后逐个关闭；ESC 可一键全关。
"""

import colorsys
import tkinter as tk
import random
import time
import sys
import math

hearts, all_wins = [], []
tips = ['学业有成', '好好爱自己', '好好吃饭', '保持好心情',
        '身体健康', '顺顺利利', '别熬夜', '天凉了多穿衣服']
colors = ['pink', 'lightblue', 'lightgreen', 'lemonchiffon',
          'hotpink', 'skyblue']
root = None


def heart_points(n, screen_w, screen_h):
    points = []
    for i in range(n):
        t = i / n * 2 * math.pi
        x = 16 * math.sin(t) ** 3
        y = (13 * math.cos(t) - 5 * math.cos(2 * t)
             - 2 * math.cos(3 * t) - math.cos(4 * t))
        sx = int(screen_w / 2 + x * 20 - 50)
        sy = int(screen_h / 2 - y * 20 - 80)
        sx = max(0, min(sx, screen_w - 150))
        sy = max(0, min(sy, screen_h - 60))
        points.append([sx, sy])
    return points


def close_all(event=None):
    for w in hearts + all_wins:
        try:
            if isinstance(w, tk.Toplevel) and w.winfo_exists():
                w.destroy()
        except tk.TclError:
            pass
    try:
        if root is not None and root.winfo_exists():
            root.destroy()
    except tk.TclError:
        pass
    sys.exit(0)


def create_popup(x, y, tip=None):
    win = tk.Toplevel()
    win.geometry(f'150x60+{x}+{y}')
    win.title('提示')
    win.attributes('-topmost', 1)
    text = tip or random.choice(tips)
    bg = random.choice(colors)
    tk.Label(win, text=text, bg=bg, font=('微软雅黑', 14), width=20, height=3).pack()
    return win


def main():
    global root
    root = tk.Tk()
    root.withdraw()
    root.bind("<Escape>", close_all)          # ESC 一键关闭所有窗口

    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    points = heart_points(100, sw, sh)

    # 第一步：依次弹出窗口拼成爱心
    for i, (x, y) in enumerate(points):
        tip = "我喜欢你" if i == len(points) - 1 else None
        win = create_popup(x, y, tip)
        hearts.append(win)
        root.update()
        time.sleep(0.03)

    time.sleep(1)
    for w in hearts:
        try:
            if w.winfo_exists():
                w.destroy()
        except tk.TclError:
            pass
    hearts.clear()

    # 第二步：满屏随机弹窗
    count = (sw // 150) * (sh // 40) + 50
    for _ in range(count):
        x = random.randint(0, sw - 150)
        y = random.randint(0, sh - 60)
        win = create_popup(x, y)
        all_wins.append(win)
        root.update()
        time.sleep(0.005)

    time.sleep(3)

    # 第三步：逐个关闭
    interval = 1.0 / len(all_wins) if all_wins else 0
    for win in all_wins:
        try:
            if win.winfo_exists():
                win.destroy()
        except tk.TclError:
            pass
        root.update()
        time.sleep(interval)
    all_wins.clear()

    try:
        root.destroy()
    except tk.TclError:
        pass


if __name__ == "__main__":
    main()
