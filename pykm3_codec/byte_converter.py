from functools import lru_cache


class ByteConverter:
    """Handles conversion between bytes and integers."""

    @staticmethod
    @lru_cache(maxsize=128)
    def to_int(data: bytes) -> int:
        """
        Convert bytes to integer using little-endian byte order.

        Args:
            data: The bytes to convert

        Returns:
            The integer representation
        """
        return int.from_bytes(data, byteorder="little")

    @staticmethod
    @lru_cache(maxsize=128)
    def from_int(value: int, length: int) -> bytes:
        """
        Convert integer to bytes using little-endian byte order.

        Args:
            value: The integer to convert
            length: The number of bytes to use

        Returns:
            The bytes representation
        """
        if value is None:
            value = 0
        return value.to_bytes(length, byteorder="little")
