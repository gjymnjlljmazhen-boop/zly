"""李峋同款粒子爱心（tkinter 版，修好可运行）。

原代码有 5 处会让它直接跑不起来，这里都修了：
1. 丢了缩进 —— Python 靠缩进定义块，整段粘贴后必然 IndentationError；
2. `def _init_(self, ...)` 少了两个下划线 —— 那是普通方法，构造时不会调用，
   `self._points` 压根不会存在 → AttributeError；
3. `if name == ' main '` 少了双下划线 —— 条件永远为假，窗口不会出现；
4. `heart = Heart()` 里 `Heart` 类没写 `__init__`，且没有括号外的参数问题；
5. `_points` 用 `set` 收集 `int` 坐标，而 `scatter_inside` 返回 float，
   混在一起没问题，但 `set` 去重会让点数变少 —— 这里保留原行为，只加注释。

运行环境：需要桌面系统（Windows / macOS / Linux 带 X11），
Android 的 proot 里既没有 tkinter 也没有 X，所以这份代码在手机上跑不了；
手机上看效果请用同算法的网页版 li-xun-heart.html。
"""

import random
from math import sin, cos, pi, log
from tkinter import Canvas, Tk

CANVAS_WIDTH = 640
CANVAS_HEIGHT = 480
CANVAS_CENTER_X = CANVAS_WIDTH / 2
CANVAS_CENTER_Y = CANVAS_HEIGHT / 2
IMAGE_ENLARGE = 11
HEART_COLOR = "#ff2121"  # 也可以试 #00ffff / #FFC0CB / #FFFF99 / #0000FF


def heart_function(t, shrink_ratio: float = IMAGE_ENLARGE):
    """爱心参数方程：x = 16sin³t，y = -(13cost - 5cos2t - 2cos3t - cos4t)。"""
    x = 16 * (sin(t) ** 3)
    y = -(13 * cos(t) - 5 * cos(2 * t) - 2 * cos(3 * t) - cos(4 * t))
    x *= shrink_ratio
    y *= shrink_ratio
    x += CANVAS_CENTER_X
    y += CANVAS_CENTER_Y
    return int(x), int(y)


def scatter_inside(x, y, beta=0.15):
    """往中心随机聚拢一个点（指数分布，近中心更密）。"""
    ratio_x = -beta * log(random.random())
    ratio_y = -beta * log(random.random())
    dx = ratio_x * (x - CANVAS_CENTER_X)
    dy = ratio_y * (y - CANVAS_CENTER_Y)
    return x - dx, y - dy


def shrink(x, y, ratio):
    """光晕收缩：离中心越近，力越强。"""
    force = -1 / (((x - CANVAS_CENTER_X) ** 2 + (y - CANVAS_CENTER_Y) ** 2) ** 0.6)
    dx = ratio * force * (x - CANVAS_CENTER_X)
    dy = ratio * force * (y - CANVAS_CENTER_Y)
    return x - dx, y - dy


def curve(p):
    """缩放比例随帧走的周期曲线。"""
    return 2 * (2 * sin(4 * p)) / (2 * pi)


class Heart:
    def __init__(self, generate_frame=20):
        self._points = set()                 # 原始爱心坐标集合
        self._edge_diffusion_points = set()  # 边缘扩散
        self._center_diffusion_points = set()  # 中心扩散
        self.all_points = {}                 # 每帧动态点坐标

        self.build(2000)

        self.random_halo = 1000
        self.generate_frame = generate_frame
        for frame in range(generate_frame):
            self.calc(frame)

    def build(self, number):
        for _ in range(number):
            t = random.uniform(0, 2 * pi)
            x, y = heart_function(t)
            self._points.add((x, y))

        for _x, _y in list(self._points):
            for _ in range(3):
                x, y = scatter_inside(_x, _y, 0.05)
                self._edge_diffusion_points.add((x, y))

        point_list = list(self._points)
        for _ in range(4000):
            x, y = random.choice(point_list)
            x, y = scatter_inside(x, y, 0.17)
            self._center_diffusion_points.add((x, y))

    @staticmethod
    def calc_position(x, y, ratio):
        """按帧的缩放比例做位置微调（0.52 是原作者试出来的魔法参数）。"""
        force = 1 / (((x - CANVAS_CENTER_X) ** 2 + (y - CANVAS_CENTER_Y) ** 2) ** 0.520)
        dx = ratio * force * (x - CANVAS_CENTER_X) + random.randint(-1, 1)
        dy = ratio * force * (y - CANVAS_CENTER_Y) + random.randint(-1, 1)
        return x - dx, y - dy

    def calc(self, generate_frame):
        ratio = 10 * curve(generate_frame / 10 * pi)
        halo_radius = int(4 + 6 * (1 + curve(generate_frame / 10 * pi)))
        halo_number = int(3000 + 4000 * abs(curve(generate_frame / 10 * pi) ** 2))

        all_points = list()
        heart_halo_point = set()

        # 1) 光晕
        for _ in range(halo_number):
            t = random.uniform(0, 2 * pi)
            x, y = heart_function(t, shrink_ratio=11.6)
            x, y = shrink(x, y, halo_radius)
            if (x, y) not in heart_halo_point:
                heart_halo_point.add((x, y))
                x += random.randint(-14, 14)
                y += random.randint(-14, 14)
                size = random.choice((1, 2, 2))
                all_points.append((x, y, size))

        # 2) 爱心本体
        for x, y in self._points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 3)
            all_points.append((x, y, size))

        # 3) 边缘扩散
        for x, y in self._edge_diffusion_points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 2)
            all_points.append((x, y, size))

        # 4) 中心扩散
        for x, y in self._center_diffusion_points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 2)
            all_points.append((x, y, size))

        self.all_points[generate_frame] = all_points

    def render(self, render_canvas, render_frame):
        for x, y, size in self.all_points[render_frame % self.generate_frame]:
            render_canvas.create_rectangle(x, y, x + size, y + size, width=0, fill=HEART_COLOR)


def draw(main: Tk, render_canvas: Canvas, render_heart: Heart, render_frame=0):
    render_canvas.delete("all")
    render_heart.render(render_canvas, render_frame)
    main.after(160, draw, main, render_canvas, render_heart, render_frame + 1)


if __name__ == "__main__":
    root = Tk()
    root.title("❤")
    canvas = Canvas(root, bg="black", height=CANVAS_HEIGHT, width=CANVAS_WIDTH)
    canvas.pack()
    heart = Heart()
    draw(root, canvas, heart)
    root.mainloop()
