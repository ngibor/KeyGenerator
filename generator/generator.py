import hashlib
import hmac

from generator.generator_util import integer_to_bytearray_converter, hmac_drgb_update


class BitGenerator:
    def __init__(self, v, key, reseed_counter):
        self.reseed_counter = reseed_counter
        self.key = key
        self.v = v

    def generate(self, requested_no_of_bits):
        if requested_no_of_bits > 7000:
            raise Exception("Too many bits requested")

        if self.reseed_counter >= 10000:
            raise Exception("Reseed required")
        temp = '0'
        while len(temp) < requested_no_of_bits:
            key = integer_to_bytearray_converter(self.key)
            v = integer_to_bytearray_converter(self.v)

            v = hmac.new(key, v, hashlib.sha256).hexdigest()
            self.v = int(''.join(format(ord(i), 'b') for i in v), 2)
            temp = int(temp, 2) | self.v
            temp = "{0:b}".format(temp)

        pseudorandom_bits = temp[:requested_no_of_bits]
        self.key, self.v = hmac_drgb_update(None, self.key, self.v)
        self.reseed_counter += 1
        return pseudorandom_bits
