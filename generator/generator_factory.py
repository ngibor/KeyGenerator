import hashlib
import hmac
from hashlib import sha256
from random import randint

from generator.generator import BitGenerator
from generator.generator_util import hmac_drgb_update


def instantiate_drgb(requested_security, personalization_string):
    if requested_security > 256:
        requested_security = 256

    if requested_security <= 112:
        requested_security = 112
    elif requested_security <= 128:
        requested_security = 128
    elif requested_security <= 192:
        requested_security = 192
    else:
        requested_security = 256

    if len(personalization_string) > 160:
        print("Personalization string is too long")
        return

    # convert personalization string to binary number
    personalization_string = ''.join(format(ord(i), 'b') for i in personalization_string)
    personalization_string = int(personalization_string, 2)

    min_entropy = 1.5 * requested_security
    entropy = get_entropy_input(min_entropy, 1000)

    #  HMAC_DRBG_Instantiate_algorithm - 7 krok
    v, key, reseed_counter = hmac_drgb_instantiate_parameters(entropy, personalization_string)

    print("# Generated parameters #")
    print("  - V :", v)
    print("  - Key:", key)
    print("  - Reseed counter: ", reseed_counter)

    return BitGenerator(v, key, reseed_counter)


def get_entropy_input(min_len, max_len):
    random_string = "some string "+ str(randint(1000000, 2000000))
    entropy = sha256(random_string.encode()).hexdigest()     # len = 403, min_len = 380
    entropy = ''.join(format(ord(i), 'b') for i in entropy)  # string hash to binary

    if len(entropy) < min_len or len(entropy) > max_len:
        print("Incorrect size of given entropy: ", len(entropy))
        return

    entropy = int(entropy, 2)  # binary string to integer
    return entropy


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






