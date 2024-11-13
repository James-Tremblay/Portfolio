import os
import sys

def egcd(a, b):
    s, t, u, v = 1, 0, 0, 1
    while b != 0:
        q = a // b
        a, b = b, a % b
        s, t, u, v = u, v, s - u * q, t - v * q
    return a, s, t


def encrypt(plaintextFile, outputFile, a, b):
    gcd, _, _ = egcd(a, 128)
    if (gcd != 1):
        print(f"The key pair ({a}, {b}) is invalid, please select another key.")
    else:
        readfile = open(plaintextFile, 'r')
        writefile = open(outputFile, 'w')
        for line in readfile:
            str = ""
            for char in line:
                str += chr((a * ord(char) + b) % 128)
            writefile.write(str)
        
def decrypt(crypticFile, outputFile, a, b):
    gcd, inverse, _ = egcd(a, 128)
    if (gcd != 1):
        print(f"The key pair ({a}, {b}) is invalid, please select another key.")
    else:
        readfile = open(crypticFile, 'r')
        writefile = open(outputFile, 'w')
        for line in readfile:
            str = ""
            for char in line:
                str += chr(((ord(char) - b + 128) * inverse) % 128)
            writefile.write(str)

def decipher(ciphertext_file, output_file, dictionary_file):
    Almostwords, outFile = open(dictionary_file, 'r'), open(output_file, 'w')
    mostWords, probKeys, decryptedString = 0, [], ""

    words = set(Almostwords.read().split())

    for a in range(1, 128):
        gcd, _, _ = egcd(a, 128)
        if (gcd != 1):
            continue
        for b in range (0, 128):
            decryptFile = "temp_decrypted.txt"
            decrypt(ciphertext_file, decryptFile, a, b)
            dfile = open(decryptFile, 'r')
            dread = dfile.read()
            valid = 0
            for word in dread.split():
                if (word.lower() in words):
                    valid += 1
            if (valid > mostWords):
                mostWords, probKeys, decryptedString = valid, (a, b), dread
    outFile.write(f"{probKeys[0]} {probKeys[1]}\n")
    outFile.write("DECRYPTED MESSAGE:\n")
    outFile.write(decryptedString)


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "encrypt":
        encrypt(sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]))
    elif mode == "decrypt":
        decrypt(sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]))
    elif mode == "decipher":
        decipher(sys.argv[2], sys.argv[3], sys.argv[4])
