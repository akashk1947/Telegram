def should_send_message(text, length, has_keyword):

    special_numbers = ["91338_17162", "98850_74380"]

    is_special = any(num in text.lower() for num in special_numbers)
    
    if is_special:
        return False
    
    if has_keyword or length > 250:
        return True

    return False