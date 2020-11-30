import math
import scipy
from scipy import special


def monobit(bin_data: str):
    count = 0

    for char in bin_data:
        if char == '0':
            count -= 1
        else:
            count += 1
    # Vypocet hodnoty p
    sobs = count / math.sqrt(len(bin_data))
    p_val = scipy.special.erfc(math.fabs(sobs) / math.sqrt(2))
    if p_val > 0.01:
        print(">> Monobit Test: PRESIEL (P val > 0.01) -->", p_val)
    else:
        print(">> Monobit Test: NEPRESIEL (P val < 0.01)  -->  ", p_val)
    return p_val