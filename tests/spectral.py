import numpy
import scipy
from scipy import special


def spectral(bin_data: str):
    n = len(bin_data)
    plus_minus_one = []
    for char in bin_data:
        if char == '0':
            plus_minus_one.append(-1)
        elif char == '1':
            plus_minus_one.append(1)
    # Produktova diskretna Fourierova transformácia plus minus jedna
    s = numpy.fft.fft(plus_minus_one)
    modulus = numpy.abs(s[0:int(n / 2)])
    tau = numpy.sqrt(numpy.log(1 / 0.05) * n)
    # Teoreticky pocet vrcholov
    count_n0 = 0.95 * (n / 2)
    # Vypocet poctu skutocnych vrcholov m> T
    count_n1 = len(numpy.where(modulus < tau)[0])
    # Vypocet statistiky hodnoty p
    d = (count_n1 - count_n0) / numpy.sqrt(n * 0.95 * 0.05 / 4)
    p_val = scipy.special.erfc(abs(d) / numpy.sqrt(2))
    if p_val > 0.01:
        print(">> Spectral Test: PRESIEL (P val > 0.01) -->", p_val)
    else:
        print(">> Spectral Test: NEPRESIEL (P val < 0.01)  -->  ", p_val)
    return p_val