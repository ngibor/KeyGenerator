from generator.generator import BitGenerator
from generator.generator_util import hmac_drgb_update


# inicializuje a vrati generator
def instantiate_drgb(entropy):





    #  HMAC_DRBG_Instantiate_algorithm - 7 krok
    v, key, reseed_counter = hmac_drgb_instantiate_parameters(entropy)

    print("# Generated parameters #")
    print("  - V :", v)
    print("  - Key:", key)
    print("  - Reseed counter: ", reseed_counter)

    return BitGenerator(v, key, reseed_counter)


def hmac_drgb_instantiate_parameters(seed_material):


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






