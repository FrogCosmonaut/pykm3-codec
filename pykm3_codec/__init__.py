"""
Pokémon Generation III Text Codec

A module for encoding and decoding text in Pokémon Generation III games.
Implements a standard Python codec for both Western and Japanese character sets.
"""
import codecs

# Import all public classes and functions from submodules
from .byte_converter import ByteConverter
from .character_maps import (
    CharacterMap,
    WesternCharacterMap,
    JapaneseCharacterMap
)
from .pk_codecs import (
    PokeTextCodec,
    WesternPokeTextCodec,
    JapanesePokeTextCodec
)
from .registry import (
    pykm3_encode,
    pykm3_decode,
    PokeStreamReader,
    PokeStreamWriter,
    pykm3_search_function
)

# Register the codec when this module is imported
codecs.register(pykm3_search_function)

# Define what symbols are exported when using "from pykm3_codec import *"
__all__ = [
    'ByteConverter',
    'CharacterMap', 
    'WesternCharacterMap', 
    'JapaneseCharacterMap',
    'PokeTextCodec', 
    'WesternPokeTextCodec', 
    'JapanesePokeTextCodec',
    'pykm3_encode',
    'pykm3_decode',
    'PokeStreamReader',
    'PokeStreamWriter',
    'pykm3_search_function'
]

# Package metadata
__version__ = '0.1.0'
__author__ = 'Juan Franco'
__email__ = 'pykm3-codec@juanfg.es'
__description__ = 'Pokémon Generation III Text Codec'