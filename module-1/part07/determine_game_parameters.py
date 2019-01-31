import hashlib
import codecs
import binascii

login = 'akorunsk'

login_sha_encrypted = hashlib.sha256(codecs.encode(login, 'ascii')).hexdigest()

ripemd160 = hashlib.new('ripemd160')
ripemd160.update(binascii.unhexlify(login_sha_encrypted))
login_sha_ripmd_encrypted = ripemd160.hexdigest()

print(login_sha_ripmd_encrypted)


coefficients = []
for i in range(1, len(login_sha_ripmd_encrypted)):
    if len(coefficients) == 3:
        break
    current = login_sha_ripmd_encrypted[-i]
    if current.isdigit():
        coefficients.append(int(current))


print("number of rounds: ", coefficients[0])
print("player replacement: ", coefficients[1])
print("error probability: ", coefficients[2])