a = "523030303237000000feff00fffe00feff00fffe00feff00fffe00feff00fffefffefffe0000fffefffefffefffefffefffe012c000000012149f00f"
a = "5230303032370000fffeff00fffe00feff00fffe00feff00fffe00feff00fffefffefffe0000fffefffefffefffefffefffe012c000000012248f00f"
print("Starting HEX String: ", a)

bTot = bytes.fromhex(a)
print("Bytes Format: ", bTot)

b = bTot[:-4]
print("Bytes Format, No Ending:", b)

thesum = 0
for byt in b:
    # print(byt)
    thesum += byt

print("Sum, DEC: ", thesum)
print("Sum, HEX: ", hex(thesum))
