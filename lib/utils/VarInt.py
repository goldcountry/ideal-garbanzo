class VarInt:
    """
    https://en.bitcoin.it/wiki/Protocol_documentation#Variable_length_integer
    """
    def __init__(self, value=0):
        self.value = None
        self.set_value(value)

    def set_value(self, value):
        self.value = value

    def to_hex(self):
        # Values < 252 are big endian; anything larger is little endian. No, I don't know why. Ask Satoshi.
        if self.value <= 0xfc:
            return self.value.to_bytes(1, byteorder="big").hex()

        # If larger than 1 byte, we need to swap endianness and prefix
        elif self.value <= 0xffff:
            prefix = 'fd'
            length = 2  # 4 bits per hex char, so a uint16 is 2 bytes

        elif self.value <= 0xffffffff:
            prefix = 'fe'
            length = 4

        elif self.value <= 0xffffffffffffffff:
            prefix = 'ff'
            length = 8

        # 64 bits is the largest possible varint, according to bitcoin reference implementation
        else:
            raise ValueError('Too large to fit into a VarInt')

        # swap endianness, convert hex to string, and pad with 0's so that the value is the correct length
        endian_swapped_value = self.value.to_bytes(length, byteorder="little")

        # Get the hex value of those bytes as a string
        hexval = endian_swapped_value.hex()

        hexval = prefix + hexval
        return hexval
