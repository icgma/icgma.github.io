# icgma.github.io · 个人网站

icgma 的个人主页：作品、工具箱、教学与联络。纯静态单文件 `index.html`，零构建、零后端、零追踪，与简历（[icgma/resume](https://github.com/icgma/resume)）同一套报刊排版视觉。

## 内容结构

| 板块 | 内容 |
|---|---|
| 报头 | 名牌 icgma + 朱红印章 + 一句话自述 |
| 数据栏 | 22 原创仓库 / 900+ 测试 / 13 在线工具 / 5 主力语言 |
| 作品 | ai-media-teaching-hub（头条）、npf-policy-narrative-analysis、media-credibility-web、slide-skill、skill-kit、NotebookLM-prompts |
| 工具箱 | 13 个可直接使用的纯前端工具（newsroom-kit 9 件 + s2t / textstats / timezone / codec） |
| 教学 | 两门课程门户 + 三个课堂演示项目 |
| 关于与联络 | 教育背景（香港大学）、研究方向、GitHub 联络 |

## 部署

1. 在 `icgma` 账号下创建名为 **`icgma.github.io`** 的公开仓库（不要初始化）。
2. 推送：

   ```bash
   git remote add origin https://github.com/icgma/icgma.github.io.git
   git push -u origin main
   ```

3. 默认即从 `main` 根目录发布，一分钟后生效：<https://icgma.github.io/>

> 注意：账号下已有 `newsroom-kit`、`codec` 等项目页部署在 `icgma.github.io/<repo>/` 子路径，本站只占用根路径，互不影响。

## 维护

- 所有内容都在 `index.html` 里，改完直接提交即可上线。
- 字体走 Google Fonts CDN（Noto Serif SC / EB Garamond / IBM Plex Mono），断网时回退系统衬线字体。
- 滚动入场动画尊重系统的「减少动态效果」设置。
