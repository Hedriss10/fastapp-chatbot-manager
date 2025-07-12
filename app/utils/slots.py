# app/utils/slots.py

EMOJI_NUMBERS = {
    1: "1️⃣",
    2: "2️⃣",
    3: "3️⃣",
    4: "4️⃣",
    5: "5️⃣",
    6: "6️⃣",
    7: "7️⃣",
    8: "8️⃣",
    9: "9️⃣",
    10: "🔟",
    0: "0️⃣",
}


def get_emoji_number(number: int) -> str:
    if 1 <= number <= 10:
        return EMOJI_NUMBERS[number]
    else:
        # For numbers greater than 10, combine emojis
        tens = number // 10
        units = number % 10
        
        tens_emoji = EMOJI_NUMBERS.get(tens, "")  # Get tens emoji or empty string
        units_emoji = EMOJI_NUMBERS.get(units, "")  # Get units emoji or empty string

        return f"{tens_emoji}{units_emoji}"