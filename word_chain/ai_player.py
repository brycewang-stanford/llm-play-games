import os
import re
import getpass
from openai import OpenAI

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

def get_ai_word(game_history, current_word, rule_type, ai_model="gpt-4o", max_retries=3):
    """
    Get AI's next word based on the word chain rules
    
    Args:
        game_history: List of previous words in the game
        current_word: The last word that AI needs to respond to
        rule_type: Type of word chain rule ('tail_to_head', 'category', 'mixed')
        ai_model: AI model to use
        max_retries: Maximum retry attempts
    
    Returns:
        String: AI's chosen word, or None if failed
    """
    if not client:
        print("OpenAI client not initialized.")
        return None
    
    # Prepare rule descriptions
    rule_descriptions = {
        'tail_to_head': "The first character of your word must match the last character of the previous word.",
        'category': "Your word must be in the same category or theme as the previous word.",
        'mixed': "You can use either tail-to-head matching OR same category/theme matching."
    }
    
    # Create the prompt
    history_text = " -> ".join(game_history) if game_history else "None"
    
    prompt = f"""You are playing a word chain game with the following rules:
{rule_descriptions.get(rule_type, rule_descriptions['tail_to_head'])}

Game History: {history_text}
Current Word: {current_word}

Please provide your next word following the rule. Your response should:
1. Be a single word or phrase (Chinese idiom, English word, or mixed)
2. Follow the specified rule
3. Be different from all previous words in the game
4. Be a real word/idiom with clear meaning

Previous words used: {', '.join(game_history)}

Response format: Just provide the word/phrase only, no explanation needed.
"""

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=ai_model,
                messages=[
                    {"role": "system", "content": "You are an expert in word games and languages. Provide only the requested word/phrase without additional explanation."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=50,
                temperature=0.7
            )
            
            ai_word = response.choices[0].message.content.strip()
            
            # Basic validation
            if ai_word and len(ai_word.split()) <= 5:  # Reasonable word length
                # Remove quotes if present
                ai_word = ai_word.strip('"\'')
                
                # Check if word is already used
                if ai_word not in game_history:
                    return ai_word
                else:
                    print(f"AI chose a repeated word: {ai_word}. Retrying...")
            else:
                print(f"AI response too long or empty: {ai_word}. Retrying...")
                
        except Exception as e:
            print(f"Error getting AI response (attempt {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                print("Retrying...")
            else:
                print("Max retries reached.")
    
    return None

def validate_word_chain(previous_word, current_word, rule_type):
    """
    Validate if current word follows the word chain rule
    
    Args:
        previous_word: The previous word in the chain
        current_word: The current word to validate
        rule_type: Type of rule to validate against
    
    Returns:
        bool: True if valid, False otherwise
    """
    if not previous_word or not current_word:
        return True  # First word is always valid
    
    prev_clean = previous_word.strip()
    curr_clean = current_word.strip()
    
    if rule_type == 'tail_to_head':
        # Check if first character of current matches last character of previous
        return prev_clean[-1] == curr_clean[0]
    elif rule_type == 'category':
        # For category matching, we'll be more lenient and allow human judgment
        # In a real implementation, this could use more sophisticated categorization
        return True
    elif rule_type == 'mixed':
        # Either tail-to-head OR category matching is acceptable
        tail_to_head_match = prev_clean[-1] == curr_clean[0]
        # For mixed mode, we assume category matching is always possible
        return tail_to_head_match or True
    
    return False
