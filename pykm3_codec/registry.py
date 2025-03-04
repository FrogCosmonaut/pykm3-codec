import codecs
from typing import Tuple, Optional


from pk_codecs import (
    WesternPokeTextCodec,
    JapanesePokeTextCodec
)
from character_maps import (
    WesternCharacterMap
)


# Python codec registration functions
def pykm3_encode(text: str, errors: str = 'strict') -> Tuple[bytes, int]:
    """
    Encode the given string using the Pokémon Generation III format.
    
    Args:
        text: The string to encode
        errors: Error handling scheme
        
    Returns:
        A tuple containing the encoded bytes and the length of the input
    """
    # Default to Western encoding
    codec = WesternPokeTextCodec()
    
    # Check for language prefix
    if text.startswith('@jp:'):
        codec = JapanesePokeTextCodec()
        text = text[4:]  # Remove prefix
    
    encoded = codec.encode(text)
    return encoded, len(text)


def pykm3_decode(data: bytes, errors: str = 'strict') -> Tuple[str, int]:
    """
    Decode the given bytes using the Pokémon Generation III format.
    
    Args:
        data: The bytes to decode
        errors: Error handling scheme
        
    Returns:
        A tuple containing the decoded string and the length of the input
    """
    # Try to determine encoding based on byte patterns
    # This is a simple heuristic - first check for characteristic Japanese bytes
    japanese_chars = set(range(0x00, 0xA1)) - set(WesternCharacterMap()._get_byte_to_char_map().keys())
    
    # If any bytes are in the Japanese-only range, use Japanese codec
    for byte in data:
        if byte in japanese_chars:
            codec = JapanesePokeTextCodec()
            break
    else:
        codec = WesternPokeTextCodec()
    
    decoded = codec.decode(data)
    return decoded, len(data)


class StreamWriter(codecs.StreamWriter):
    """Stream writer for the pykm3 codec."""

    encode = pykm3_encode


class StreamReader(codecs.StreamReader):
    """Stream reader for the pykm3 codec."""

    decode = pykm3_decode


def pykm3_search_function(encoding: str) -> Optional[codecs.CodecInfo]:
    """
    Search function for the pykm3 codec.
    
    Args:
        encoding: The encoding name
        
    Returns:
        CodecInfo if the encoding matches, None otherwise
    """
    if encoding.lower() in ('pykm3', 'pykm3-codec'):
        return codecs.CodecInfo(
            name='pykm3',
            encode=pykm3_encode,
            decode=pykm3_decode,
            streamreader=StreamReader,
            streamwriter=StreamWriter,
        )
    return None