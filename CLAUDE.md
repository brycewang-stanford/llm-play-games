# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an AI gaming battle platform featuring multiple classic games where different LLM models compete against each other or play against humans. The project demonstrates strategic gameplay capabilities of various AI models through turn-based games.

## Repository Structure

```
/
├── gomoku/           # Five-in-a-row game implementation
├── word_chain/       # Chinese idiom chain game
├── splendor/         # Splendor game (incomplete)
└── README.md         # Project documentation
```

## Common Commands

### Running Games

Each game is run independently from its respective directory:

**Gomoku (Five-in-a-row):**
```bash
cd gomoku
python3 gomoku.py                    # AI vs AI mode
python3 gomoku_human_vs_ai.py        # Human vs AI mode
```

**Word Chain (Chinese Idiom Chain):**
```bash
cd word_chain
python3 word_chain_ai_vs_ai.py       # AI vs AI mode
python3 word_chain_human_vs_ai.py    # Human vs AI mode
```

**Splendor:**
```bash
cd splendor
python3 splendor_game.py             # Basic game (incomplete)
```

### Dependencies

Install required dependencies for each game:
```bash
# For Gomoku
cd gomoku && pip install -r requirements.txt

# For Word Chain
cd word_chain && pip install -r requirements.txt
```

All games require `openai>=1.0.0` for LLM integration.

## Architecture

### Game Structure Pattern

Each game follows a consistent modular architecture:

1. **Main Game File**: Core game logic, board management, and game loop
2. **AI Player Module**: OpenAI API integration and AI decision-making
3. **Human vs AI Mode**: Separate script for human player interaction

### Common AI Implementation

All games share these AI integration patterns:

- **Client Initialization**: Automatic environment variable detection with manual fallback
- **Retry Logic**: 3-attempt retry mechanism for handling API failures
- **Model Configuration**: Easy model switching via dictionaries (e.g., `PLAYER_MODELS`)
- **Response Parsing**: Regex-based parsing of AI responses with validation

### Game Flow Architecture

1. **Initialization**: Board setup and AI client initialization
2. **Game Loop**: Turn-based player alternation with move validation
3. **Win Detection**: Game-specific win condition checking
4. **Error Handling**: Graceful handling of invalid moves and API failures

## Key Implementation Details

### OpenAI Integration

- **API Key Management**: Supports both environment variables and manual input
- **Error Handling**: Comprehensive error handling for API failures and invalid responses
- **Model Selection**: Easy switching between different OpenAI models (gpt-4o, gpt-4o-mini)

### Game-Specific Features

**Gomoku:**
- 15x15 board with coordinate system (0,0) to (14,14)
- Win condition: 5 pieces in a row (horizontal, vertical, diagonal)
- Move limit: 100 moves per player

**Word Chain:**
- Chinese idiom chain game with strict character matching
- Rule: Last character of previous idiom must match first character of next
- Supports multiple rule variations and scoring systems

**Splendor:**
- Multi-player game simulation (incomplete implementation)
- Note: Currently incomplete as rules are being clarified

### Development Patterns

- **No Testing Framework**: No automated tests are configured
- **No Build System**: Pure Python scripts, no build process required
- **No Linting**: No code quality tools configured
- **Manual Execution**: All games run via direct Python script execution

## API Key Configuration

All games require OpenAI API access. Set up using either:

1. **Environment Variable** (recommended):
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

2. **Manual Input**: Games will prompt for API key if environment variable not found

## Development Notes

- Each game is self-contained within its directory
- Games can be run independently without cross-dependencies
- All AI decision-making uses OpenAI's chat completion API
- Game state is managed in-memory (no persistence)
- Console-based user interface for all games

## Status

- **Gomoku**: Fully implemented and tested
- **Word Chain**: Functional with comprehensive rule validation
- **Splendor**: Incomplete - author clarifying official rules