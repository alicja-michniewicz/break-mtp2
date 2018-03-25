from message.cracker2 import Cracker
from message.data_loader import load_ciphertexts_from_file

ciphertexts = load_ciphertexts_from_file("texts.txt")

cracker = Cracker(ciphertexts)

print(ciphertexts[0])
cracker.crack()
cracker.guess()