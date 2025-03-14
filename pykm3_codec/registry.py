import codecs
from typing import Optional, Tuple
from functools import lru_cache

from .pk_codecs import JapanesePokeTextCodec, WesternPokeTextCodec

# Create singleton instances once - avoid recreation
_JAPANESE_CODEC = JapanesePokeTextCodec()
_WESTERN_CODEC = WesternPokeTextCodec()

# Pre-define constants
_EMPTY_RESULT = ("", 0)
_PYKM3_NAMES = frozenset(("pykm3", "pykm3codec"))
_PYKM3JAP_NAMES = frozenset(("pykm3jap", "pykm3japanese"))


def register() -> None:
    """Register the codec search function once."""
    codecs.register(pykm3_search_function)


@lru_cache(maxsize=512)
def pykm3_encode(
    text: str, errors: str = "strict", final: bool = False
) -> Tuple[bytes, int]:
    """
    Encode the given string using the Pokémon Generation III format.
    Default to Western encoding, with automatic detection for Japanese.

    Args:
        text: The string to encode
        errors: Error handling scheme
        final: Flag indicating if this is the final chunk

    Returns:
        A tuple containing the encoded bytes and the length of the input
    """
    encoded = _WESTERN_CODEC.encode(text, errors)
    return encoded, len(text)


@lru_cache(maxsize=512)
def pykm3_jap_encode(
    text: str, errors: str = "strict", final: bool = False
) -> Tuple[bytes, int]:
    """
    Encode the given string using the Pokémon Generation III Japanese format.
    Always uses Japanese encoding regardless of content.

    Args:
        text: The string to encode
        errors: Error handling scheme
        final: Flag indicating if this is the final chunk

    Returns:
        A tuple containing the encoded bytes and the length of the input
    """
    return _JAPANESE_CODEC.encode(text, errors), len(text)


@lru_cache(maxsize=512)
def pykm3_decode(
    data: bytes, errors: str = "strict", final: bool = False
) -> Tuple[str, int]:
    """
    Decode the given bytes using the Pokémon Generation III western format.

    Args:
        data: The bytes to decode
        errors: Error handling scheme
        final: Flag indicating if this is the final chunk

    Returns:
        A tuple containing the decoded string and the length of the input
    """
    if not data:
        return _EMPTY_RESULT
    return _WESTERN_CODEC.decode(data, errors), len(data)


@lru_cache(maxsize=512)
def pykm3_jap_decode(
    data: bytes, errors: str = "strict", final: bool = False
) -> Tuple[str, int]:
    """
    Decode the given bytes using the Pokémon Generation III Japanese format.

    Args:
        data: The bytes to decode
        errors: Error handling scheme
        final: Flag indicating if this is the final chunk

    Returns:
        A tuple containing the decoded string and the length of the input
    """
    if not data:
        return _EMPTY_RESULT
    return _JAPANESE_CODEC.decode(data, errors), len(data)


class PokeStreamWriter(codecs.StreamWriter):
    """Base stream writer for the pykm3 codec."""

    def __init__(self, stream, encode_func, errors="strict"):
        super().__init__(stream, errors)
        self.encode_func = encode_func

    def write(self, text):
        """Write the given text to the stream."""
        if not isinstance(text, str):
            text = str(text)

        encoded_data, length = self.encode_func(text, self.errors)
        self.stream.write(encoded_data)
        return length


class PokeStreamReader(codecs.StreamReader):
    """Base stream reader for the pykm3 codec."""

    def __init__(self, stream, decode_func, errors="strict"):
        super().__init__(stream, errors)
        self.decode_func = decode_func

    def decode(self, input, errors="strict"):
        """Decode input using the pykm3 codec."""
        return self.decode_func(input, errors)


# Factory functions to create the appropriate reader/writer classes
def create_stream_writer(stream, errors="strict", japanese=False):
    """Create a stream writer with the appropriate encoding function."""
    encode_func = pykm3_jap_encode if japanese else pykm3_encode
    return PokeStreamWriter(stream, encode_func, errors)


def create_stream_reader(stream, errors="strict", japanese=False):
    """Create a stream reader with the appropriate decoding function."""
    decode_func = pykm3_jap_decode if japanese else pykm3_decode
    return PokeStreamReader(stream, decode_func, errors)


# Define codec info singletons
_WEST_CODEC_INFO = codecs.CodecInfo(
    name="pykm3",
    encode=pykm3_encode,
    decode=pykm3_decode,
    streamreader=lambda stream, errors="strict": create_stream_reader(
        stream, errors, japanese=False
    ),
    streamwriter=lambda stream, errors="strict": create_stream_writer(
        stream, errors, japanese=False
    ),
)

_JAP_CODEC_INFO = codecs.CodecInfo(
    name="pykm3jap",
    encode=pykm3_jap_encode,
    decode=pykm3_jap_decode,
    streamreader=lambda stream, errors="strict": create_stream_reader(
        stream, errors, japanese=True
    ),
    streamwriter=lambda stream, errors="strict": create_stream_writer(
        stream, errors, japanese=True
    ),
)


def pykm3_search_function(encoding: str) -> Optional[codecs.CodecInfo]:
    """Search function for the pykm3 codec."""
    if encoding.lower() in _PYKM3_NAMES:
        return _WEST_CODEC_INFO
    if encoding.lower() in _PYKM3JAP_NAMES:
        return _JAP_CODEC_INFO
    return None
