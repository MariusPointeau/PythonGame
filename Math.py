def is_integer(str):
    try:
        int(str)
        return True
    except ValueError:
        return False
    
def Check_String_Input(str, possibilities) -> int:
    text_to_return = str
    if not is_integer(text_to_return):
        while not is_integer(text_to_return) or int(text_to_return) > possibilities:
            text_to_return = input("Please entre a number :")
    return int(text_to_return)