# 爱心页面合集

三个纯前端页面，无依赖、无构建，双击即可打开；也可以直接挂 GitHub Pages。

| 页面 | 说明 |
|---|---|
| [`index.html`](index.html) | 粒子爱心（李峋同款）：Canvas 逐行复刻 tkinter 版算法——爱心参数方程、光晕收缩、边缘/中心扩散、20 帧 @160ms 的心跳 |
| [`big-heart.html`](big-heart.html) | 全屏大爱心：CSS 心形 + 双峰心跳 + 呼吸光晕，点按炸开小爱心并触发振动 |
| [`popup.html`](popup.html) | 爱心弹窗：毛玻璃卡片 + Canvas 爱心粒子，点击空白处冒一颗，支持 Esc 关闭 |

## 参数速查

- 粒子爱心：`IMAGE_ENLARGE = 11`、`HEART_COLOR = "#ff2121"`、`FRAME_MS = 160`、`GENERATE_FRAME = 20`，
  以及两个「魔法参数」`0.6`（光晕收缩）与 `0.520`（逐帧位移）。
- 大爱心：心跳 `@keyframes thump`（1.35s）、尺寸 `min(72vmin, 460px)`。
- 弹窗：粒子上限 260，`dt` 截断 0.05s，尊重 `prefers-reduced-motion`。

## Python 版

`heart_tk.py` 是原始的 tkinter 实现（修好缩进与 4 个 bug 的版本），需要桌面系统才能跑：

```sh
python3 heart_tk.py
```

Android 的 proot 里既没有 tkinter 也没有 X 显示，跑不了，请用网页版。
