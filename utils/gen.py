import random
import string

def generate_random_string(length=0) -> str:
    """Generate a random string of fixed length."""
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))