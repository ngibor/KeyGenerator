from hashlib import sha256
from random import randint

from entropy.EntropyCalculating import get_entropy_from_string, get_entropy_random_org, get_entropy_from_system
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


def ask_key_len():

    while True:
        KEY_MENU_TEXT = """
        Vyberte delku klice
        **************************
        stisknutím 1) zvolite 128b
        stisknutím 2) zvolite 192b
        stisknutím 3) zvolite 256b
        stisknutím 4) zvolite 512b
        **************************
                    """
        print(KEY_MENU_TEXT)
        input_text_menu = int(input())

        if input_text_menu == 1:
            return 128
        elif input_text_menu == 2:
            return 192
        elif input_text_menu == 3:
            return 256
        elif input_text_menu == 4:
            return 512
        else:
            print("     Spatne zadane cislo")
            continue


def ask_entropy_type():

    ENTROPIE_TEXT = """ 
        Instalace generatoru,
        Způsob získávání entropii  
        *****************************************************
        stisknutím 1) ziskavani entropie z operacniho systemu
        stisknutím 2) ziskavani entropie ze stringu uzivatele
        stisknutím 3) ziskavani entropie z random.org
        *****************************************************
        """
    while True:
        print(ENTROPIE_TEXT)
        input_text_menu = int(input())

        if input_text_menu == 1:
            return get_entropy_from_system()
        elif input_text_menu == 2:
            print('zadejte text pro vypocet entropie')
            ent_str = str(input())
            return get_entropy_from_string(ent_str)
        elif input_text_menu == 3:
            try:
                return get_entropy_random_org()
            except:
                print('Chyba připojení internetu, prosím, zkontrolujte svoje internetové připojení a zkuste to znovu')
        else:
            print("Spatne zadane cislo")
            continue


def print_key(key: str):
    FORMAT_TEXT = """ 
        Vyberte spusob formatovani
        **************************
        stisknutím 1) Binarni
        stisknutím 2) Decimalni
        stisknutím 3) Hexadecimalni
    
        **************************
    """
    while True:
        print(FORMAT_TEXT)
        input_text_menu = int(input())
        if input_text_menu == 1:
            print(key)
        elif input_text_menu == 2:
            print(int(key, 2))
        elif input_text_menu == 3:
            print(hex(int(key, 2)))
        else:
            print("Spatne zadane cislo")
            continue
        return


def test_generator(key_len):
    print('Zacinam testy pro ', key_len, ' bitu ...')
    monobit_success = 0
    spectral_success = 0
    for i in range(10):
        test_string = generator.generate(key_len)
        if monobit(test_string):
            monobit_success += 1
        if spectral(test_string):
            spectral_success += 1
    print('Monobit pro ', key_len, ' bitu prosel ', monobit_success, '/10')
    print('Spectral pro ', key_len, ' bitu prosel ', spectral_success, '/10')


if __name__ == "__main__":

    MENU_TEXT = """
        MENU
        **************************
        stisknutím 1) Vygenerovat klic
        stisknutím 2) Testovat generator
        stisknutím 3) Udelat reseed
        stisknutím 4) Ukoncit program
        **************************
        """

    requested_security = 256  # maximalni pro sha256, minimalni je 112
    min_entropy = 1.5 * requested_security

    while True:

        entropy = ask_entropy_type()
        generator = instantiate_drgb(entropy)

        while True:

            print(MENU_TEXT)
            option = int(input())

            if option == 1:
                keyLen = ask_key_len()
                try:
                    generated_key = generator.generate(keyLen)
                except ReseedException:
                    print('Reseedováni je nutné')
                    break
                print_key(generated_key)
            elif option == 2:
                try:
                    test_generator(128)
                    test_generator(256)
                    test_generator(512)
                except ReseedException:
                    print('Reseedováni je nutné')
                    break
            elif option == 3:
                break
            elif option == 4:
                exit()
            else:
                print('Spatne zadane cislo')









