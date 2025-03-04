from .character_maps import (
    CharacterMap,
    WesternCharacterMap,
    JapaneseCharacterMap
)


class PokeTextCodec:
    """Base class for Pokémon text codecs."""
    
    def __init__(self, char_map: CharacterMap):
        """
        Initialize the codec with a character map.
        
        Args:
            char_map: The character map to use
        """
        self.char_map = char_map
    
    def encode(self, text: str, errors: str = 'strict') -> bytes:
        """
        Encode a string into Pokémon text format.
        
        Args:
            text: The string to encode
            
        Returns:
            The encoded bytes
        """
        result = bytearray()

        for char in text:
            if char == '\n':
                result.append(self.char_map.LINE_BREAK)
            elif char in self.char_map.char_to_byte:
                result.append(self.char_map.char_to_byte[char])
            else:
                # If character not found, use space as fallback
                result.append(self.char_map.char_to_byte.get(' ', 0x00))
                
        # Add terminator
        result.append(self.char_map.TERMINATOR)
        return bytes(result)
    
    def decode(self, data: bytes, errors: str = 'strict') -> str:
        result = []
        i = 0
        
        while i < len(data):
            byte = data[i]
            
            if byte == self.char_map.TERMINATOR:
                break  # Stop at terminator
            elif byte == self.char_map.LINE_BREAK:
                result.append('\n')
            elif byte in self.char_map.byte_to_char:
                result.append(self.char_map.byte_to_char[byte])
            else:
                # Handle unknown bytes according to the errors parameter
                if errors == 'strict':
                    raise UnicodeDecodeError('pykm3', data, i, i+1, f"Invalid byte: {byte}")
                elif errors == 'replace':
                    result.append('?')
                elif errors == 'ignore':
                    pass  # Skip this byte
                else:
                    # Default fallback
                    result.append('?')
            
            i += 1
                
        return ''.join(result)


class WesternPokeTextCodec(PokeTextCodec):
    """Codec for Western Pokémon text."""
    
    def __init__(self):
        """Initialize with Western character map."""
        super().__init__(WesternCharacterMap())


class JapanesePokeTextCodec(PokeTextCodec):
    """Codec for Japanese Pokémon text."""
    
    def __init__(self):
        """Initialize with Japanese character map."""
        super().__init__(JapaneseCharacterMap())