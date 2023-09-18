f = open("encoded.txt", "rb")
for a in f:
    print(bin(int(a)), end='') 