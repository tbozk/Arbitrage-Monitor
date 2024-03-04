from TRADE_SYMBOLS import symbols

with open('PAIRS_EXTRACTED', 'r') as f:
    pair_data = f.read()

# Convert string to Python list
pair_list = eval(pair_data)


directed_list = {}


for symbol in symbols:
    directed_list[symbol] = []

for pair in pair_list:
    s=""
    c=""
    bl = False
    for ch in pair:
        if(bl):
            c+=ch
            continue
        s+=ch
        if s in symbols:
            bl=True

    if c in symbols:
        directed_list[s].append(c)


all_triplets = []

for A in directed_list:
    lst = []
    for B in directed_list[A]:
        if B not in symbols:
            lst.append(B)

    for l in lst:
        directed_list[A].remove(l)



for A in directed_list:
    for B in directed_list[A]:
        for C in directed_list[B]:
            if C in directed_list[A]:
                all_triplets.append([A, B, C])




print(all_triplets)




with open('ALL_TRIPLETS.txt', 'w') as f:
    for triplet in all_triplets:
        concatenated_triplet = [triplet[0]+triplet[1], triplet[1]+triplet[2], triplet[0]+triplet[2]]
        for i in range(0,2):
            if concatenated_triplet[i] not in pair_list:
                print("ERROR, PAIR DOESNT EXIST")
        f.write(str(concatenated_triplet) + '\n')




