# videodeck

[English](README.md) · [工作流](docs/workflow.md) · [验证记录](docs/validation.md)

把文章、项目材料或脚本制作成能独立讲清机制的视频。延续
[postdeck](https://github.com/OpenMedia-Lab/postdeck) 的交互确认方式，专注视频制作。

HyperFrames 负责渲染；[caption-cli](https://github.com/OpenMedia-Lab/caption-cli)
在本地准备带时间码的画面、音频和审阅任务；当前 Agent 或 subagent 负责理解和判断。
skill 本身不要求第三方模型 API、云端账号或付费视频服务。配音工具可替换，本地 ASR 可选；
Agent 宿主、模型和发布平台有各自的运行条件。

## 安装

```bash
git clone https://github.com/OpenMedia-Lab/videodeck.git
mkdir -p "$HOME/.codex/skills"
videodeck_target="$HOME/.codex/skills/videodeck"
test ! -e "$videodeck_target" && test ! -L "$videodeck_target" &&
  ln -s "$PWD/videodeck/videodeck" "$videodeck_target"
```

如已安装，先检查原目录，避免覆盖。其他兼容 Agent Skills 的宿主可安装仓库内层
`videodeck/` 到其技能目录；部分宿主支持 `~/.agents/skills`。不依赖其他 skill。

示例：“用 $videodeck 把这篇文章做成面向工程师的横屏技术视频，沿用已确认声线与风格，
保留公式，先本地交付。”

## 工作方式

只补问会影响结果的缺项，复用已经明确的答案。先理清目标和粗分镜；旁白复用已选声线或先
试听，做上下文读音试样，再生成主音轨、按真实声音细化时间。新视觉方向先看代码关键帧与
独立封面，新运动语言先看完整动作和转场的编码样片，确认后制作整片。默认采用清楚、成本低的
2D；只有必要空间关系难以用2D讲清时才局部使用3D。极简配色不降低构造、排版和动态细节要求。
数学小标签与公式一并排版，局部修复保留已确认转场。Agent 实际审片并修复，再交用户审阅。

旁白跨镜头保持完整；显示术语与发音别名分开；字幕用原稿，ASR 核对漏词与改词，
字面相同不能证明多音字、缩写的音值正确。
“只打磨转场”会锁定原有旁白、公式与例子。有问题就定位来源、解码、时间线或编码层，
补静音不能修复缺掉的尾音。

投稿前独立展示每条视频完整的标题、简介、分区、标签、可见性，等待真实确认。
简介保留实际换行，投稿后回读文案、媒体、合集顺序及平台状态。

## 工程与验证

主 skill 只保留顺序、关键门槛和阶段路由，声音、分镜、艺术方向、HyperFrames、审片和发布
细节按需读取。提供一个固定依赖的可运行小样、可选黑白灰加单一强调色的技术风格配置，
以及 Python 标准库实现的时间线校验与 SRT 导出工具。

```bash
python3 -m unittest discover -s tests -v
python3 videodeck/scripts/timeline.py check /path/to/timeline.json
```

画面采样覆盖与连续播放、原生试听分别记录；工具退出成功不等于内容、音质或审美已通过。
实际运行版本、检查结果与能力限制见[验证记录](docs/validation.md)。不打包私人声线、账号、
教程视频或大型模型。MIT 协议。
