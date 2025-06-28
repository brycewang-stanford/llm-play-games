# 🔗 Word Chain Game | 词语接龙游戏

[English](#english) | [中文](#中文)

---

## English

### Game Introduction

This is an intelligent Word Chain Game featuring multiple game modes and rule variations:
1. **AI vs AI**: Two different OpenAI models competing against each other
2. **Human vs AI**: Human players versus AI opponents

The game supports various word chain rules including Chinese idioms, English words, and mixed language gameplay with flexible rule systems.

### 🌟 Key Features

- **Multiple Rule Types**: Tail-to-head matching, category matching, or mixed rules
- **AI vs AI Battle**: GPT-4o vs GPT-4o-mini intelligent word chain competition
- **Human vs AI Mode**: Challenge AI opponents with your vocabulary skills
- **Multilingual Support**: Chinese idioms, English words, and mixed language gameplay
- **Real-time Display**: Clear game progress visualization
- **Smart Validation**: Automatic rule checking and word repetition detection
- **Scoring System**: Points tracking and performance statistics

### 🎮 Game Rules

#### Rule Types
1. **Tail-to-Head (首尾相接)**: The first character of your word must match the last character of the previous word
2. **Same Category (同类词语)**: Your word must be in the same category or theme as the previous word
3. **Mixed Rules (混合规则)**: Either tail-to-head OR category matching is acceptable

#### Scoring
- **+1 point** for each valid word played
- **+5 bonus points** when opponent fails to find a valid word
- **Game ends** when maximum rounds reached or a player cannot continue

### 🚀 Quick Start

#### Requirements
- Python 3.7+
- OpenAI API Key

#### Installation

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
   
   **Human vs AI Mode:**
   ```bash
   python3 word_chain_human_vs_ai.py
   
   # Custom max rounds (default: 100)
   python3 word_chain_human_vs_ai.py 50
   ```
   
   **AI vs AI Battle Mode:**
   ```bash
   python3 word_chain_ai_vs_ai.py
   
   # Custom max rounds (default: 100)
   python3 word_chain_ai_vs_ai.py 30
   ```

### 🎯 Game Screenshots

**Human vs AI Mode:**
```
🎯 Word Chain Game - Round 5/50
📊 Score - Human: 4 | AI: 4
📜 Rule: Tail-to-Head (首尾相接)
============================================================
📖 Game History: 智慧 -> 慧眼 -> 眼光 -> 光明 -> 明天 -> 天空 -> 空间 -> 间隔
🎯 Current Word: 隔离

👤 Your turn!
Enter your word (or 'quit' to exit): 离开
✅ You played: 离开
```

**AI vs AI Battle:**
```
🤖 AI vs AI Word Chain Battle - Round 8/30
📊 Score - GPT-4o: 7 | GPT-4o-mini: 6
📜 Rule: Mixed Rules (混合规则)
======================================================================
📖 Game History: 开始 -> 始终 -> 终点 -> 点燃 -> 燃烧 -> 烧饭 -> 饭店 -> 店铺
🎯 Current Word: 铺路

🤖 GPT-4o is thinking...
🤖 GPT-4o played: 路径
```

### 🛠️ Technical Implementation

#### Core Files
- `word_chain_human_vs_ai.py`: Human vs AI game mode
- `word_chain_ai_vs_ai.py`: AI vs AI battle mode
- `ai_player.py`: AI decision making and OpenAI API interaction
- `requirements.txt`: Python dependencies

#### Key Features
- **Intelligent Word Generation**: AI analyzes context and rules to generate appropriate words
- **Rule Validation**: Automatic checking of word chain rules and constraints
- **Game State Management**: Comprehensive tracking of game progress and statistics
- **Error Handling**: Robust handling of AI failures and invalid inputs
- **Multi-language Support**: Handles Chinese, English, and mixed language input

#### AI Strategy Components
- **Context Analysis**: AI considers game history and current word
- **Rule Compliance**: Ensures generated words follow selected game rules
- **Vocabulary Diversity**: Avoids repetition and maintains word variety
- **Strategic Thinking**: Balances rule compliance with creative word selection

### 🎲 Gameplay Strategies

**For Human Players:**
- **Vocabulary Building**: Expand your knowledge of idioms and words
- **Pattern Recognition**: Learn common character combinations
- **Category Thinking**: Group words by themes and relationships
- **Strategic Planning**: Consider both offense and defense

**AI Capabilities:**
- **Rule Adherence**: Perfect compliance with game rules
- **Creative Responses**: Generates diverse and contextually appropriate words
- **Memory Management**: Avoids repetition across long game sessions
- **Adaptive Strategy**: Adjusts approach based on game progress

### 📈 Game Flow

1. **Setup**: Choose rule type and starting word
2. **Turn-based Play**: Alternating moves between players
3. **Validation**: Automatic checking of rules and constraints
4. **Scoring**: Points awarded for valid moves
5. **Game End**: Results display with complete game history

### 🔧 Customization

You can easily customize the game by:
- Modifying `MAX_ROUNDS` for game length
- Changing AI models in `PLAYER_MODELS` dictionary
- Adding new rule types in validation functions
- Implementing custom scoring systems
- Adding language-specific word databases

---

## 中文

### 游戏简介

这是一个智能词语接龙游戏，支持多种游戏模式和规则变化：
1. **AI vs AI**: 两个不同的OpenAI模型互相对战
2. **Human vs AI**: 人类玩家与AI对战

游戏支持多种词语接龙规则，包括中文成语、英文单词和混合语言游戏，具有灵活的规则系统。

### 🌟 特色功能

- **多种规则类型**: 首尾相接、同类词语或混合规则
- **AI vs AI对战**: GPT-4o vs GPT-4o-mini 智能词语接龙竞赛
- **人机对战模式**: 用您的词汇技能挑战AI对手
- **多语言支持**: 中文成语、英文单词和混合语言游戏
- **实时显示**: 清晰的游戏进度可视化
- **智能验证**: 自动规则检查和词语重复检测
- **计分系统**: 积分跟踪和性能统计

### 🎮 游戏规则

#### 规则类型
1. **首尾相接**: 您的词语首字符必须与前一个词语的末字符相同
2. **同类词语**: 您的词语必须与前一个词语属于同一类别或主题
3. **混合规则**: 首尾相接或同类词语规则均可接受

#### 计分规则
- **+1分** 每个有效词语
- **+5分** 当对手无法找到有效词语时的奖励分数
- **游戏结束** 当达到最大轮数或玩家无法继续时

### 🚀 快速开始

#### 环境要求
- Python 3.7+
- OpenAI API 密钥

#### 安装步骤

1. **安装依赖**
   ```bash
   pip install openai
   ```

2. **设置API密钥**
   ```bash
   # 方法1：环境变量
   export OPENAI_API_KEY="your-api-key-here"
   
   # 方法2：运行时输入
   # 游戏会提示您输入API密钥
   ```

3. **启动游戏**
   
   **人机对战模式:**
   ```bash
   python3 word_chain_human_vs_ai.py
   
   # 自定义最大轮数（默认：100）
   python3 word_chain_human_vs_ai.py 50
   ```
   
   **AI vs AI 对战模式:**
   ```bash
   python3 word_chain_ai_vs_ai.py
   
   # 自定义最大轮数（默认：100）
   python3 word_chain_ai_vs_ai.py 30
   ```

### 🎯 游戏截图

**人机对战模式:**
```
🎯 Word Chain Game - Round 5/50
📊 Score - Human: 4 | AI: 4
📜 Rule: Tail-to-Head (首尾相接)
============================================================
📖 Game History: 智慧 -> 慧眼 -> 眼光 -> 光明 -> 明天 -> 天空 -> 空间 -> 间隔
🎯 Current Word: 隔离

👤 Your turn!
Enter your word (or 'quit' to exit): 离开
✅ You played: 离开
```

**AI对战模式:**
```
🤖 AI vs AI Word Chain Battle - Round 8/30
📊 Score - GPT-4o: 7 | GPT-4o-mini: 6
📜 Rule: Mixed Rules (混合规则)
======================================================================
📖 Game History: 开始 -> 始终 -> 终点 -> 点燃 -> 燃烧 -> 烧饭 -> 饭店 -> 店铺
🎯 Current Word: 铺路

🤖 GPT-4o is thinking...
🤖 GPT-4o played: 路径
```

### 🛠️ 技术实现

#### 核心文件
- `word_chain_human_vs_ai.py`: 人机对战游戏模式
- `word_chain_ai_vs_ai.py`: AI vs AI 对战模式
- `ai_player.py`: AI决策和OpenAI API交互
- `requirements.txt`: Python依赖包

#### 关键特性
- **智能词语生成**: AI分析上下文和规则生成合适的词语
- **规则验证**: 自动检查词语接龙规则和约束条件
- **游戏状态管理**: 全面跟踪游戏进度和统计信息
- **错误处理**: 稳健处理AI失败和无效输入
- **多语言支持**: 处理中文、英文和混合语言输入

#### AI策略组件
- **上下文分析**: AI考虑游戏历史和当前词语
- **规则遵循**: 确保生成的词语遵循选定的游戏规则
- **词汇多样性**: 避免重复并保持词语多样性
- **策略思维**: 平衡规则遵循与创意词语选择

### 🎲 游戏策略

**对人类玩家:**
- **词汇积累**: 扩展您的成语和词语知识
- **模式识别**: 学习常见字符组合
- **分类思维**: 按主题和关系对词语分组
- **策略规划**: 考虑攻守兼备

**AI能力:**
- **规则遵循**: 完美遵循游戏规则
- **创意回应**: 生成多样化且上下文合适的词语
- **记忆管理**: 在长游戏会话中避免重复
- **自适应策略**: 根据游戏进度调整方法

### 📈 游戏流程

1. **设置**: 选择规则类型和起始词语
2. **轮流游戏**: 玩家之间交替移动
3. **验证**: 自动检查规则和约束条件
4. **计分**: 为有效移动授予积分
5. **游戏结束**: 显示结果和完整游戏历史

### 🔧 自定义设置

您可以轻松自定义游戏:
- 修改 `MAX_ROUNDS` 调整游戏长度
- 在 `PLAYER_MODELS` 字典中更改AI模型
- 在验证函数中添加新规则类型
- 实现自定义计分系统
- 添加特定语言的词语数据库

---

**Enjoy the intelligent word chain battle!** 🎮✨
**享受智能词语接龙对战！** 🎮✨
