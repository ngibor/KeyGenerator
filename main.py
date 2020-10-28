from hashlib import sha256
from random import randint

from generator.generator_factory import instantiate_drgb


# funkce pro zkuseni, musi vratit integer, velikost ktereho lezi mezi min_len a max_len (v bitech)
# minimalni delka je 1.5 * requested security, coz je pro nas 1.5 * 256
# maximalni delka je 1000
def get_entropy_input(min_len, max_len):
    random_string = "some string " + str(randint(1000000, 2000000))
    entropy = sha256(random_string.encode()).hexdigest()     # len = 403, min_len = 380
    entropy = ''.join(format(ord(i), 'b') for i in entropy)  # string hash to binary

    if len(entropy) < min_len or len(entropy) > max_len:
        raise Exception("Incorrect size of given entropy")

    entropy = int(entropy, 2)  # binary string to integer
    return entropy


if __name__ == "__main__":

    requested_security = 256                    # maximalni pro sha256, minimalni je vsak 112
    min_entropy = 1.5 * requested_security
    generator = instantiate_drgb("personalization string (is optional)", get_entropy_input(min_entropy, 1000))
    for i in range(10):
        number = int(generator.generate(128), 2)
        print(number)




