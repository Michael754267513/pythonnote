import random
# import string


def gen_random_string(char_set, length):
    if not hasattr(gen_random_string, "rng"):
        gen_random_string.rng = random.SystemRandom()   # Create a static variable
    return ''.join([gen_random_string.rng.choice(char_set) for _ in xrange(length)])

# password_charset = string.ascii_letters + string.digits
# print gen_random_string(password_charset, 16)
