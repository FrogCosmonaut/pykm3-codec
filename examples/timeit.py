import timeit

import pykm3_codec

pykm3_codec.register()
codec = pykm3_codec.WesternPokeTextCodec()


def timeit_decorator(func):
    def wrapper(*args, **kwargs):
        elapsed_time = timeit.timeit(lambda: func(*args, **kwargs), number=1)
        print(f"{func.__name__} took {elapsed_time:.6f} seconds")
        return func(*args, **kwargs)

    return wrapper


@timeit_decorator
def test_encode_with_codec(text: str):
    for _ in range(10_000_000):
        codec.encode(text)


@timeit_decorator
def test_encode_with_register(text: str):
    for _ in range(10_000_000):
        text.encode("pykm3")


# Western text
text = "Hello trainer!"
test_encode_with_codec(text)
test_encode_with_register(text)
