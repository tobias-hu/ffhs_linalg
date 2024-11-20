"""
Created on: 13.11.2025
Author: Tobias Gasche
Description: Main file for playing with HammingCode Class
"""

from HammingCode import HammingCode

codeInstance = HammingCode(3)

encoded = codeInstance.encode(1011)
print("Encoded: ", encoded)

if codeInstance.check_codeword(encoded):
    print("Codeword is valid")
else:
    print("Codeword is not valid")

encodedWithError = codeInstance.bitFlip(encoded, 4)
print("Encoded with Bitflip: ", encodedWithError)

if codeInstance.check_codeword(encodedWithError):
    print("Codeword is valid")
else:
    print("Codeword is not valid")

correctedword = codeInstance.getCorrection(encodedWithError)
print("Corrected Word: ", correctedword)

decoded = codeInstance.decode(correctedword)
print("Decoded word: ", decoded)

print(codeInstance.get_generator_matrix())
print(codeInstance.get_check_matrix())
