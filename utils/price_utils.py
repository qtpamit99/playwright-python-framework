def extract_price(text):
    return int("".join(filter(str.isdigit, text)))
