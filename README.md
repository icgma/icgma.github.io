# icgma.github.io · 个人网站

icgma 的个人网站，多页面结构（真实 URL 切换 + 空闲/悬停预加载）：关于 / 课程 / 软件 / 进行中 / 资源。中英一键切换，纯静态、零构建、零追踪。

## 页面

| 页面 | 文件 | 内容 |
|---|---|---|
| 关于 | `index.html` | 第一人称学术自传、研究方向、教育背景、简历链接 |
| 课程 | `courses.html` | 智能传媒制作（JOU2327A）、编程基础 |
| 软件 | `software.html` | ai-media-teaching-hub、npf-policy-narrative-analysis、slide-skill、newsroom-kit、media-credibility-web、skill-kit |
| 进行中 | `working.html` | NPF 信度工作流、课程材料开源化、工具箱维护 |
| 资源 | `resources.html` | 13 个在线即用工具 + 3 个课堂演示项目 |

共享资源：`assets/style.css`（纸墨视觉系统）、`assets/site.js`（语言切换 / 入场动画 / 预加载）。

## 字体

- **中文**：自托管 Noto Serif SC 子集（`assets/fonts/noto-serif-sc-subset.woff2`，426 字，字重轴 200–900 可变，134 KB 单文件）。不走 Google Fonts，因此中国大陆可正常显示。
- **拉丁 / 等宽**：EB Garamond 与 IBM Plex Mono 仍由 Google Fonts 提供。

子集是按当前文案裁剪的快照。**修改任何可见文字后**需重跑：

```
python tools/build-cjk-subset.py
```

未重跑时，新增字符会回退到系统衬线字体，与周围的子集字明显不同。脚本依赖 `fonttools` 与 `brotli`。字体许可证见 `assets/fonts/OFL.txt`。

## 预加载

- 浏览器空闲时（`requestIdleCallback`）自动为其余四个页面注入 `<link rel="prefetch" as="document">`；
- 悬停 / 聚焦 / 触摸导航链接时立即预取目标页；
- 页面均为 10KB 级纯 HTML，预取后切换近乎即时。

## 维护

- 每个页面独立 HTML，改哪页提交哪页，`git push` 后 Pages 自动构建。
- 语言切换：导航栏 EN / 中文 按钮，选择记忆于 localStorage，全站生效。
- 新增页面：拷贝任一页面骨架，改 `data-title-zh/en`，把导航链接加进各页导航栏，并把文件名加进 `assets/site.js` 的 `PAGES` 数组。改了文案还要重跑字体子集脚本（见上）。

## 部署

`icgma.github.io` 用户页仓库，推送 `main` 即发布：<https://icgma.github.io/>
