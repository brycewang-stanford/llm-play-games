# 🎮 LLM Play Games | AI游戏对战平台

[English](#english) | [中文](#中文)

## 🏆 Battle Results | 对战结果

| Game | Mode | Player 1 | Player 2 | Score | Win Rate | Status |
|------|------|----------|----------|-------|----------|--------|
| Gomoku (五子棋) | AI vs AI | GPT-4o | GPT-4o-mini | 100:0 | 100% | ✅ Tested |
| Gomoku (五子棋) | Human vs AI | Human | GPT-4o | 1:10 | 9.1% | ✅ Tested |
| Word Chain (成语接龙) | AI vs AI | GPT-4o | GPT-4o-mini | -:- | - | 🛑 Testing |
| Word Chain (成语接龙) | Human vs AI | Human | GPT-4o | -:- | - | 🛑 Testing |
| Chinese Chess | AI vs AI | - | - | -:- | - | 🛑 Coming Soon |
| Go | AI vs AI | - | - | -:- | - | 🛑 Coming Soon |
| Chess | AI vs AI | - | - | -:- | - | 🛑 Coming Soon |

> **Note**: Test results are based on multiple game sessions. Individual results may vary.
> 
> **说明**: 测试结果基于多轮游戏对战。单次结果可能有所不同。

---

## English

### Project Introduction

An open-source project focused on AI gaming battles using Large Language Models (LLM) technology. Implements intelligent gameplay in classic games with multiple game modes:
- 🤖 **AI vs AI**: Two different AI models competing against each other
- 👤 **Human vs AI**: Human players versus AI opponents
- 👥 **Multi-model Comparison**: Testing strategic capabilities of different AI models

### 🌟 Key Features

- **Multi-model Support**: Supports OpenAI GPT-4o, GPT-4o-mini, and other models
- **Real-time Battles**: Clear console interface with real-time game status
- **Intelligent Decision Making**: AI analyzes game situations and makes strategic decisions
- **Easy Extension**: Modular design for easy addition of new games

### 🎯 Implemented Games

#### 1. Gomoku (Five in a Row)
Location: `/gomoku`

Classic Gomoku game supporting both AI vs AI and Human vs AI modes.

**Game Features:**
- Standard 15×15 board
- First to connect five wins
- Maximum 100 moves per player
- Intelligent defense and attack strategies
- Two game modes: AI vs AI and Human vs AI

#### 2. Chinese Idiom Chain Game (成语接龙)
Location: `/word_chain`

Intelligent Chinese idiom chain game with strict tail-to-head character matching rules.

**Game Features:**
- Strict rule: Last character of previous idiom must exactly match first character of next idiom
- Four-character Chinese idioms (成语) only
- Two game modes: AI vs AI and Human vs AI
- Smart validation and scoring system
- Real-time game progress visualization
- Duplicate idiom detection
- Cultural and linguistic challenge

**Technical Highlights:**
- Clear game state visualization
- Smart idiom validation and character matching
- Detailed game history tracking
- Multi-retry mechanism ensuring effective AI responses
- Chinese character encoding support

**Running Example:**
```
=============================================
  第 5/100 轮 | 人类: 3 分 | AI: 2 分
  当前成语: 龙飞凤舞 | 下一个必须以'舞'开头
=============================================
📖 游戏历史: 一心一意 -> 意气风发 -> 发愤图强 -> 强词夺理 -> 理直气壮
🎯 当前成语: 龙飞凤舞
💡 提示: 下一个成语必须以 '舞' 开头
```

### 🚀 Quick Start

#### Requirements
- Python 3.7+
- OpenAI API Key

#### Installation & Running

1. **Clone the Repository**
   ```bash
   git clone https://github.com/brycewang-stanford/llm-play-games.git
   cd llm-play-games
   ```

2. **Set up API Key**
   ```bash
   # Method 1: Environment Variable
   export OPENAI_API_KEY="your-api-key-here"
   
   # Method 2: Input during runtime
   # The program will prompt for API key input
   ```

3. **Run Games**
   
   **Gomoku - AI vs AI Mode:**
   ```bash
   cd gomoku
   python3 gomoku.py
   ```
   
   **Gomoku - Human vs AI Mode:**
   ```bash
   cd gomoku
   python3 gomoku_human_vs_ai.py
   ```
   
   **Word Chain - AI vs AI Mode:**
   ```bash
   cd word_chain
   python3 word_chain_ai_vs_ai.py
   ```
   
   **Word Chain - Human vs AI Mode:**
   ```bash
   cd word_chain
   python3 word_chain_human_vs_ai.py
   ```

### 📋 Roadmap

- [ ] **Chinese Chess**: Traditional Chinese chess AI battles
- [ ] **Go**: 9×9 or 19×19 Go game battles
- [ ] **Chess**: Classic international chess
- [ ] **Tic-Tac-Toe**: Simple strategy game
- [ ] **Connect Four**: Vertical connection game
- [ ] **Human vs AI Mode**: Support for human player participation ✅ (Available in Gomoku)

### 🛠️ Tech Stack

- **Language**: Python 3.7+
- **AI Models**: OpenAI GPT-4o / GPT-4o-mini
- **API**: OpenAI API
- **Architecture**: Modular design

### 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 中文

### 项目简介

这是一个专注于人工智能游戏对战的开源项目。使用大语言模型（LLM）技术，实现经典游戏中的智能对战，支持多种游戏模式：
- 🤖 **AI vs AI**: 两个不同的AI模型互相对战
- 👤 **Human vs AI**: 人类玩家与AI对战
- 👥 **多模型比较**: 测试不同AI模型的策略能力

### 🌟 特色功能

- **多模型支持**: 支持 OpenAI GPT-4o、GPT-4o-mini 等多种模型
- **实时对战**: 清晰的控制台界面，实时显示游戏状态
- **智能决策**: AI能够分析棋局，做出策略性决策
- **易于扩展**: 模块化设计，方便添加新游戏

### 🎯 已实现游戏

#### 1. 五子棋 (Gomoku)
位置：`/gomoku`

经典的五子棋游戏，支持AI vs AI和Human vs AI两种模式。

**游戏特点：**
- 15×15 标准棋盘
- 先连成五子者获胜
- 每位玩家最多100步
- 智能防守与进攻策略
- 两种游戏模式：AI vs AI 和 Human vs AI

#### 2. 成语接龙游戏 (Chinese Idiom Chain)
位置：`/word_chain`

智能成语接龙游戏，严格的字字相接规则，具有挑战性。

**游戏特点：**
- 严格规则：上一个成语的最后一个字必须与下一个成语的第一个字完全相同
- 只能使用四字成语
- 两种游戏模式：AI vs AI 和 Human vs AI
- 智能验证和计分系统
- 实时游戏进度可视化
- 重复成语检测
- 文化和语言挑战

**技术亮点：**
- 清晰的游戏状态可视化显示
- 智能的成语验证与字符匹配
- 详细的游戏状态追踪
- 多轮重试机制确保AI响应有效
- 中文字符编码支持

**运行示例：**
```
=============================================
  第 5/100 轮 | 人类: 3 分 | AI: 2 分
  当前成语: 龙飞凤舞 | 下一个必须以'舞'开头
=============================================
📖 游戏历史: 一心一意 -> 意气风发 -> 发愤图强 -> 强词夺理 -> 理直气壮
🎯 当前成语: 龙飞凤舞
💡 提示: 下一个成语必须以 '舞' 开头
```

### 🚀 快速开始

#### 环境要求
- Python 3.7+
- OpenAI API 密钥

#### 安装与运行

1. **克隆项目**
   ```bash
   git clone https://github.com/brycewang-stanford/llm-play-games.git
   cd llm-play-games
   ```

2. **设置API密钥**
   ```bash
   # 方法1：环境变量
   export OPENAI_API_KEY="your-api-key-here"
   
   # 方法2：程序运行时输入
   # 运行程序时会提示输入API密钥
   ```

3. **运行游戏**
   
   **五子棋 - AI vs AI 模式:**
   ```bash
   cd gomoku
   python3 gomoku.py
   ```
   
   **五子棋 - 人机对战模式:**
   ```bash
   cd gomoku
   python3 gomoku_human_vs_ai.py
   ```
   
   **成语接龙 - AI vs AI 模式:**
   ```bash
   cd word_chain
   python3 word_chain_ai_vs_ai.py
   ```
   
   **成语接龙 - 人机对战模式:**
   ```bash
   cd word_chain
   python3 word_chain_human_vs_ai.py
   ```

### 📋 后续计划

- [ ] **象棋 (Chinese Chess)**: 传统中国象棋AI对战
- [ ] **围棋 (Go)**: 9×9或19×19围棋对战
- [ ] **国际象棋 (Chess)**: 经典国际象棋
- [ ] **井字棋 (Tic-Tac-Toe)**: 简单策略游戏
- [ ] **四子棋 (Connect Four)**: 垂直连线游戏
- [ ] **人机对战模式**: 支持人类玩家参与 ✅ (五子棋已实现)

### 🛠️ 技术栈

- **语言**: Python 3.7+
- **AI模型**: OpenAI GPT-4o / GPT-4o-mini
- **API**: OpenAI API
- **架构**: 模块化设计

### 🤝 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

### 📞 Contact

Project Link: [https://github.com/brycewang-stanford/llm-play-games](https://github.com/brycewang-stanford/llm-play-games)

⭐ If this project helps you, please give it a star!
⭐ 如果这个项目对你有帮助，请给它一个星标！

---

> **Note**: The Splendor game in this repository is incomplete as the author is still clarifying the official rules.
