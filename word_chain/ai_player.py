import os
import re
import getpass
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Client Initialization ---
api_key = os.environ.get("OPENAI_API_KEY")
client = None

if api_key:
    try:
        client = OpenAI(api_key=api_key)
        print("OpenAI client initialized using environment variable.")
    except Exception as e:
        print(f"Error initializing OpenAI client with environment variable: {e}")
else:
    print("OPENAI_API_KEY environment variable not found.")

def initialize_client_manually():
    """Initialize OpenAI client manually if environment variable is not set"""
    global client
    if client:
        return True
    
    try:
        manual_key = getpass.getpass("Please enter your OpenAI API key: ")
        if manual_key.strip():
            client = OpenAI(api_key=manual_key.strip())
            print("OpenAI client initialized manually.")
            return True
        else:
            print("No API key provided.")
            return False
    except Exception as e:
        print(f"Error initializing OpenAI client manually: {e}")
        return False

def get_ai_idiom(game_history, current_idiom, ai_model="gpt-4o", max_retries=3):
    """
    Get AI's next Chinese idiom for idiom chain game
    
    Args:
        game_history: List of previous idioms in the game
        current_idiom: The last idiom that AI needs to respond to
        ai_model: AI model to use
        max_retries: Maximum retry attempts
    
    Returns:
        String: AI's chosen idiom, or None if failed
    """
    if not client:
        print("OpenAI client not initialized.")
        return None
    
    # Create the prompt for Chinese idiom chain
    history_text = " -> ".join(game_history) if game_history else "无"
    
    prompt = f"""你正在玩成语接龙游戏，规则如下：
1. 你必须提供一个四字成语
2. 你的成语的第一个字必须与上一个成语的最后一个字完全相同
3. 你的成语不能与之前使用过的成语重复
4. 必须是真实存在的中文成语

游戏历史: {history_text}
当前成语: {current_idiom}

已使用的成语: {', '.join(game_history)}

请只回答下一个成语，不要任何解释。
"""

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=ai_model,
                messages=[
                    {"role": "system", "content": "你是一个成语专家，精通中文成语接龙游戏。只提供所需的成语，不要额外解释。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=20,
                temperature=0.7
            )
            
            ai_idiom = response.choices[0].message.content.strip()
            
            # Basic validation for Chinese idiom
            if ai_idiom and len(ai_idiom) == 4 and all('\u4e00' <= char <= '\u9fff' for char in ai_idiom):
                # Remove quotes if present
                ai_idiom = ai_idiom.strip('"\'')
                
                # Check if idiom is already used
                if ai_idiom not in game_history:
                    return ai_idiom
                else:
                    print(f"AI选择了重复的成语: {ai_idiom}. 重试中...")
            else:
                print(f"AI回应不是四字成语: {ai_idiom}. 重试中...")
                
        except Exception as e:
            print(f"获取AI回应时出错 (第 {attempt + 1} 次尝试): {e}")
            if attempt < max_retries - 1:
                print("重试中...")
            else:
                print("已达到最大重试次数.")
    
    return None

def validate_idiom_chain(previous_idiom, current_idiom):
    """
    Validate if current idiom follows the idiom chain rule
    
    Args:
        previous_idiom: The previous idiom in the chain
        current_idiom: The current idiom to validate
    
    Returns:
        bool: True if valid, False otherwise
    """
    if not previous_idiom or not current_idiom:
        return True  # First idiom is always valid
    
    # Both must be 4-character Chinese idioms
    if len(previous_idiom) != 4 or len(current_idiom) != 4:
        return False
    
    if not (all('\u4e00' <= char <= '\u9fff' for char in previous_idiom) and 
            all('\u4e00' <= char <= '\u9fff' for char in current_idiom)):
        return False
    
    # Check if last character of previous matches first character of current
    return previous_idiom[-1] == current_idiom[0]
