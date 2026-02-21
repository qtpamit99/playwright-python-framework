import random
import string

def generate_order_data():
    rand = ''.join(random.choices(string.ascii_letters, k=5))

    return {
        "name": f"AutoUser_{rand}",
        "country": "India",
        "city": "Bangalore",
        "card": str(random.randint(10000000, 99999999)),
        "month": str(random.randint(1, 12)),
        "year": str(random.randint(2026, 2035))
    }
