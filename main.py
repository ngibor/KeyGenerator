from hashlib import sha256
from random import randint

from entropy.EntropyCalculating import get_entropy_from_string, get_entropy_random_org
from generator.generator import ReseedException
from generator.generator_factory import instantiate_drgb


# funkce pro zkuseni, musi vratit integer, velikost ktereho lezi mezi min_len a max_len (v bitech)
# minimalni delka je 1.5 * requested security, coz je pro nas 1.5 * 256
# maximalni delka je 1000
from tests.monobit import monobit
from tests.spectral import spectral


def get_entropy_input(min_len, max_len):
    random_string = "some string " + str(randint(1000000, 2000000))
    entropy = sha256(random_string.encode()).hexdigest()     # delka v bitech = 403, minimalne potrebujeme 380
    entropy = ''.join(format(ord(i), 'b') for i in entropy)  # string hash to binary

    if len(entropy) < min_len or len(entropy) > max_len:
        raise Exception("Incorrect size of given entropy")

    entropy = int(entropy, 2)  # binary string to integer
    print('entropy in example', entropy)
    return entropy


if __name__ == "__main__":


    requested_security = 256                    # maximalni pro sha256, minimalni je 112
    min_entropy = 1.5 * requested_security

    # Vrati pripraveny BitGenerator
    generator = instantiate_drgb("personalization string (is optional)", get_entropy_input(min_entropy, 1000))


    # generuje 128 bitu, prevadi do integeru a printuje integer
    for i in range(10):
        try:
            test_string = generator.generate(512)
            monobit(test_string)
            spectral(test_string)
        except ReseedException:
            print('Reseed is required')
            generator = instantiate_drgb("personalization string (is optional)", get_entropy_input(min_entropy, 1000))




