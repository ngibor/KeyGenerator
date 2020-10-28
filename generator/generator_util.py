import hashlib
import hmac


def integer_to_bytearray_converter(number):
    number = "{0:b}".format(number)
    bit_padding = len(number) % 8
    number = "0" * bit_padding + number
    byte_array = bytearray()

    for i in range(int(len(number) / 8)):
        string_byte = number[i * 8: i * 8 + 8]
        byte_array.append(int(string_byte, 2))

    return byte_array


def hmac_drgb_update(data, k, v):

    if data is not None:
        v = v | 0x00 | data

    k_as_bytes = integer_to_bytearray_converter(k)                       # potrebujeme bytearray v hmac
    v_as_bytes = integer_to_bytearray_converter(v)                       # potrebujeme bytearray v hmac

    k = hmac.new(k_as_bytes, v_as_bytes, hashlib.sha256).hexdigest()

    k = int(''.join(format(ord(i), 'b') for i in k), 2)         # string to binary int
    k_as_bytes = integer_to_bytearray_converter(k)                       # potrebujeme bytearray v hmac

    v = hmac.new(k_as_bytes, v_as_bytes, hashlib.sha256).hexdigest()
    v = int(''.join(format(ord(i), 'b') for i in v), 2)         # string to binary in

    if data is None:
        return k, v

    v = v | 0x01 | data

    v_as_bytes = integer_to_bytearray_converter(v)                       # potrebujeme bytearray v hmac

    k = hmac.new(k_as_bytes, v_as_bytes, hashlib.sha256).hexdigest()   # hmac(k, v)

    k = int(''.join(format(ord(i), 'b') for i in k), 2)       # string to binary int
    k_as_bytes = integer_to_bytearray_converter(k)

    v = hmac.new(k_as_bytes, v_as_bytes, hashlib.sha256).hexdigest()
    v = int(''.join(format(ord(i), 'b') for i in v), 2)       # string to binary int

    return k, v
