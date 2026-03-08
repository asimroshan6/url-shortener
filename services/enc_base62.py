ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
BASE = len(ALPHABET)


def encode_base62(num: int) -> str:
    if num == 0:
        return ALPHABET[0]

    result = []

    while num > 0:
        remainder = num % BASE
        result.append(ALPHABET[remainder])
        num //= BASE

    result.reverse()
    return "".join(result)
