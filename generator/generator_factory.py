import hashlib
import hmac
from hashlib import sha256
from random import randint

from generator.generator import BitGenerator
from generator.generator_util import hmac_drgb_update


# inicializuje a vrati generator
def instantiate_drgb(personalization_string, entropy):

    if len(personalization_string) > 160:
        raise Exception("Personalization string is too long")

    # convert personalization string to binary number
    personalization_string = ''.join(format(ord(i), 'b') for i in personalization_string)
    personalization_string = int(personalization_string, 2)

    #  HMAC_DRBG_Instantiate_algorithm - 7 krok
    v, key, reseed_counter = hmac_drgb_instantiate_parameters(entropy, personalization_string)

    print("# Generated parameters #")
    print("  - V :", v)
    print("  - Key:", key)
    print("  - Reseed counter: ", reseed_counter)

    return BitGenerator(v, key, reseed_counter)


def hmac_drgb_instantiate_parameters(entropy, personalization):
    seed_material = entropy | personalization

    key = ""
    for i in range(256):         # outlen = 256 pro sha256
        key += "0"
    key = int(key, 2)            # string to binary

    v = ""
    for i in range(int(256 / 8)):
        v += "00000001"             # 00000001 = 0x01 = 1
    v = int(v, 2)                # string to binary

    key, v = hmac_drgb_update(seed_material, key, v)
    reseed_counter = 1
    return v, key, reseed_counter






