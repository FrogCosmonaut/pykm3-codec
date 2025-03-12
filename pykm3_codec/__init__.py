"""
Pokémon Generation III Text Codec

A module for encoding and decoding text in Pokémon Generation III games.
Implements a standard Python codec for both Western and Japanese characters.
"""
from .byte_converter import ByteConverter
from .pk_codecs import JapanesePokeTextCodec, WesternPokeTextCodec
from .registry import register


# Define what symbols are exported when using "from pykm3_codec import *"
__all__ = ["ByteConverter", "WesternPokeTextCodec", "JapanesePokeTextCodec", "register"]

# Package metadata
__version__ = "0.5.1"
__author__ = "Juan Franco"
__email__ = "pykm3-codec@juanfg.es"
__description__ = "Pokémon Generation III Text Codec"
