# https://chatgpt.com/c/683ad42b-72c0-800d-b769-40ac072430b6

# ✅ rule_engine.py
# python
# Copy
# Edit
def rule_based_reply(text: str, emotion: str) -> str:
    if "?" in text:
        return "That’s a good question 😄 What do you think about it?"
    if emotion == "joy":
        return "Haha you sound happy! Tell me more ☺️"
    if emotion == "sadness":
        return "Oh no 😢 Wanna talk about it?"
    return "Mmm interesting… go on!"