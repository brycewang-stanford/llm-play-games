# 🏹 Gomoku AI Battle | 五子棋AI对战

[English](#english) | [中文](#中文)

---

## English

### Game Introduction

This is a Gomoku AI battle game featuring two game modes:
1. **AI vs AI**: Two different OpenAI models competing against each other
2. **Human vs AI**: Human players versus AI opponents

The game uses a standard 15×15 board where the first player to connect five pieces wins.

### 🌟 Key Features

- **AI vs AI Battle**: GPT-4o vs GPT-4o-mini intelligent gameplay
- **Human vs AI Battle**: Human players compete against AI opponents
- **Real-time Display**: Clear console interface showing board state
- **Smart Decision Making**: AI analyzes board positions and makes strategic decisions
- **Error Handling**: Multiple validation layers ensure valid AI moves
- **Game Statistics**: Real-time display of each player's move count

### 🎮 Game Rules

1. **Board**: Standard 15×15 Gomoku board
2. **Win Condition**: First to connect 5 pieces horizontally, vertically, or diagonally
3. **Move Limit**: Maximum 100 moves per player
4. **Piece Symbols**: Player 1 = X, Player 2 = O

### 🚀 Quick Start

#### Requirements
- Python 3.7+
- OpenAI API Key

#### Running the Game

1. **Install Dependencies**
   ```bash
   pip install openai
   ```

2. **Set up API Key**
   ```bash
   # Method 1: Environment Variable
   export OPENAI_API_KEY="your-api-key-here"
   
   # Method 2: Runtime Input
   # The game will prompt you to enter your API key
   ```

3. **Start the Game**
   
   **AI vs AI Battle Mode:**
   ```bash
   python3 gomoku.py
   ```
   
   **Human vs AI Battle Mode:**
   ```bash
   python3 gomoku_human_vs_ai.py
   ```

### 🎯 Game Screenshot

```
=============================================
  You (X): 5/100 | AI (O): 4/100
=============================================
   0  1  2  3  4  5  6  7  8  9  10 11 12 13 14
  +---------------------------------------------+
0 |  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . |
1 |  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . |
2 |  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . |
3 |  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . |
4 |  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . |
5 |  .  .  .  .  X  X  .  .  .  .  .  .  .  .  . |
6 |  .  O  O  O  X  O  X  X  O  X  O  O  .  .  . |
7 |  .  .  .  .  .  .  O  X  O  .  .  .  .  .  . |
8 |  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . |
...
```

### 🛠️ Technical Implementation

#### Core Files
- `gomoku.py`: AI vs AI main game logic and interface
- `gomoku_human_vs_ai.py`: Human vs AI battle mode
- `ai_player.py`: AI decision making and OpenAI API interaction

#### Key Features
- **Intelligent Prompt System**: Provides clear board state descriptions to AI
- **Position Validation**: Ensures AI chooses valid and unoccupied positions
- **Error Retry**: Up to 3 retry attempts for handling AI response errors
- **Game State Tracking**: Real-time monitoring of game progress and win conditions

### 🎲 AI Battle Strategies

The AI demonstrates strategic capabilities including:
- **Offensive Strategy**: Attempts to form threatening connections
- **Defensive Strategy**: Blocks opponent's five-in-a-row attempts
- **Position Optimization**: Selects strategic board positions
- **Board Analysis**: Understands current game state

### 📈 Game Flow

1. **Initialization**: Set up board and initialize AI clients
2. **Turn-based Play**: Alternating moves between Player 1 (X) and Player 2 (O)
3. **Move Validation**: Verify each AI move is legal and valid
4. **Win Detection**: Check for five-in-a-row after each move
5. **Game End**: Declare winner or draw condition

### 🔧 Customization

You can easily customize the game by:
- Changing AI models in `PLAYER_MODELS` dictionary
- Adjusting board size (default: 15×15)
- Modifying move limits
- Adding new AI providers beyond OpenAI

---

## 中文

### 游戏简介

这是一个五子棋AI对战游戏，支持两种对战模式：
1. **AI vs AI**: 两个不同的OpenAI模型进行智能对战
2. **Human vs AI**: 人类玩家与AI对战

游戏采用标准的15×15棋盘，先连成五子者获胜。

### 🌟 特色功能

- **AI vs AI对战**: GPT-4o vs GPT-4o-mini 智能对战
- **Human vs AI对战**: 人类玩家与AI智能对战
- **实时游戏显示**: 清晰的控制台界面显示棋盘状态
- **智能决策**: AI能够分析棋局并做出策略性决策
- **错误处理**: 多重验证确保AI移动的有效性
- **游戏统计**: 实时显示每位玩家的移动次数

### 🎮 游戏规则

1. **棋盘**: 15×15标准五子棋棋盘
2. **获胜条件**: 率先在横、竖、斜方向连成5个棋子
3. **移动限制**: 每位玩家最多100步
4. **棋子标识**: Player 1 = X, Player 2 = O

### 🚀 快速开始

#### 环境要求
- Python 3.7+
- OpenAI API密钥

#### 运行游戏

1. **安装依赖**
   ```bash
   pip install openai
   ```

2. **设置API密钥**
   ```bash
   # 方法1: 环境变量
   export OPENAI_API_KEY="your-api-key-here"
   
   # 方法2: 运行时输入
   # 游戏会提示你输入API密钥
   ```

3. **启动游戏**
   
   **AI vs AI 对战模式:**
   ```bash
   python3 gomoku.py
   ```
   
   **Human vs AI 对战模式:**
   ```bash
   python3 gomoku_human_vs_ai.py
   ```

### 🎯 游戏截图

```
=============================================
  Player 1 (X): 5/100 | Player 2 (O): 4/100
            Turn: Player 1 (gpt-4o-mini)           
=============================================
   0  1  2  3  4  5  6  7  8  9  10 11 12 13 14
  +---------------------------------------------+
0 |  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . |
1 |  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . |
2 |  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . |
3 |  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . |
4 |  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . |
5 |  .  .  .  .  X  X  .  .  .  .  .  .  .  .  . |
6 |  .  O  O  O  X  O  X  X  O  X  O  O  .  .  . |
7 |  .  .  .  .  .  .  O  X  O  .  .  .  .  .  . |
8 |  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . |
...
```

### 🛠️ 技术实现

#### 核心文件
- `gomoku.py`: AI vs AI 主游戏逻辑和界面
- `gomoku_human_vs_ai.py`: Human vs AI 对战模式
- `ai_player.py`: AI决策和OpenAI API交互

#### 关键特性
- **智能提示系统**: 为AI提供清晰的棋盘状态描述
- **位置验证**: 确保AI选择的位置有效且未被占用
- **错误重试**: 最多3次重试机制处理AI响应错误
- **游戏状态追踪**: 实时监控游戏进度和获胜条件

### 🎲 AI对战策略

游戏中的AI展现了以下策略能力：
- **进攻策略**: 尝试形成连线威胁
- **防守策略**: 阻止对手形成五连
- **位置优化**: 选择战略性位置
- **局面分析**: 理解当前棋局状态

---

> **Note**: The Splendor game in this repository is incomplete as the author is still clarifying the official rules.