import unicodedata


def emoji_to_hex_string(emoji):
    normalized_emoji = unicodedata.normalize('NFC', emoji)
    code_points = [ord(char) for char in normalized_emoji]
    hex_string = '-'.join([f'u{cp:04X}' for cp in code_points]).lower()
    return hex_string


def hex_string_to_emoji(hex_string):
    code_points = hex_string.replace('u', '').split('-')
    characters = [chr(int(cp, 16)) for cp in code_points]
    emoji = ''.join(characters)
    return emoji
