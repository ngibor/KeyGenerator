import math
import hashlib
import random
import requests


# entropy z os
def get_entropy_from_system():
    data = random.SystemRandom().randint(2 ** 380, 2 ** 1000)
    return data


def get_entropy_from_string(string):
    # Spocitaji entropie

    # spocita pravdepodobnost char v string
    prob = [float(string.count(c)) / len(string) for c in dict.fromkeys(list(string))]

    # Spocitaji entropie
    entropy = - sum([p * math.log(p) / math.log(2.0) for p in prob])

    entropy = hashlib.sha256(str(entropy).encode()).hexdigest()  # hashujeme, aby dostat delku, kterou potrebujeme
    entropy = ''.join(format(ord(i), 'b') for i in entropy)  # prevadime string hash do binarniho stringu (0 a 1)

    if len(entropy) < 380 or len(entropy) > 1000:  # jestli delka je spatna, error
        raise Exception("Incorrect size of given entropy")

    entropy = int(entropy, 2)  # binary string to integer

    print('entropy: ', entropy)
    return entropy


def get_entropy_random_org():
    # random org rest api url
    url = 'https://api.random.org/json-rpc/2/invoke'

    # telo post requestu, pouzil jsem svuj apiKey
    body = {
        'jsonrpc': '2.0',
        'method': 'generateBlobs',
        'params': {
            'apiKey': '1b4700a1-9f7e-4ee6-a49e-6d6ee1006989',
            'n': 1,
            'size': 800,
            'format': 'hex'
        },
        'id': 42}

    # delame post request
    response = requests.post(url=url, json=body)

    # dostavame json odpoved'
    response_data = response.json()

    # potrebujeme jen jednu polozku z odpovedi
    entropy = str(response_data['result']['random']['data'])

    # nahodne cislo je ve tvaru ['cislo'], zbavim se od [' a ']
    entropy = entropy[2:-2]

    # diky 'format': 'hex' v requestu, nahodne bity dostaneme ve formatu hex cisla
    # prevedeme stringove hex cislo na puvodni cislo
    entropy = int(entropy, 16)

    return entropy
