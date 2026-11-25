# icgma.github.io · 个人网站

icgma 的个人网站，多页面结构（真实 URL 切换 + 空闲/悬停预加载）：关于 / 课程 / 软件 / 进行中 / 资源（附 `404.html`）。中英无闪烁切换，纯静态、零构建、零外部请求、零追踪。

## 页面

| 页面 | 文件 | 内容 |
|---|---|---|
| 关于 | `index.html` | 第一人称学术自传、研究方向、教育背景 |
| 课程 | `courses.html` | 智能传媒制作（JOU2327A）、编程基础 |
| 软件 | `software.html` | ai-media-teaching-hub、npf-policy-narrative-analysis、slide-skill、newsroom-kit、media-credibility-web、skill-kit |
| 进行中 | `working.html` | NPF 信度工作流、课程材料开源化、工具箱维护 |
| 资源 | `resources.html` | 13 个在线即用工具 + 3 个课堂演示项目 |
| 404 | `404.html` | 纸墨风兜底页（根路径引用，兼容深层失效链接） |

共享资源：`assets/style.css`（纸墨视觉系统与中英分治排版）、`assets/site.js`（语言切换 / 入场动画 / 预加载）。

## 字体（100% 自托管）

- **中文**：Noto Serif SC 可变字重子集（`assets/fonts/noto-serif-sc-subset.woff2`，字重轴 200–900）。
- **拉丁衬线**：EB Garamond 正/斜可变字重拉丁子集（`eb-garamond-latin.woff2`、`eb-garamond-italic-latin.woff2`，字重轴 400–800）。
- **等宽**：IBM Plex Mono 拉丁子集（`ibm-plex-mono-400-latin.woff2`、`ibm-plex-mono-500-latin.woff2`）。

全站不发起任何 Google Fonts 请求，中国大陆与海外均可直接首屏渲染。

中文子集是按当前可见文案裁剪的快照。**修改任何可见中文文字后**需重跑：

```bash
python tools/build-cjk-subset.py
```

如需连同拉丁与等宽子集一并重生成，加 `--all` 参数。脚本依赖 `fonttools` 与 `brotli`，字体许可证见 `assets/fonts/OFL.txt`。

## 预加载与语言记忆

- `<head>` 内置极小同步脚本，首帧绘制前读取 `localStorage` 并锁定 `html.en`，跨页跳转零中文闪屏；
- 浏览器空闲时（`requestIdleCallback`）自动为其余页面注入 `<link rel="prefetch" as="document">`，悬停 / 聚焦 / 触摸导航链接时立即预取；
- 页面均为数 KB 纯 HTML，预取后切换近乎即时。

## 维护与部署

- 每个页面独立 HTML，改哪页提交哪页，`git push` 后 Pages 自动构建。
- 新增页面：拷贝任一页面骨架，改 `data-title-zh/en` 与 `aria-current="page"`，把导航链接同步进各页导航栏；改了中文文案后重跑 `python tools/build-cjk-subset.py`。
- 部署于 `icgma.github.io` 用户页仓库，推送 `main` 即发布：<https://icgma.github.io/>
