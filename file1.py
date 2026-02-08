import math
def huffman(probas):
    n = len(probas)
    codes = [""] * n
    arbre_probas = probas.copy()
    arbre_codes = [str(i) for i in range(n)]
    while len(arbre_probas) > 1:
        min1 = arbre_probas.index(min(arbre_probas))
        temp = arbre_probas[min1]
        arbre_probas[min1] = float('inf')
        min2 = arbre_probas.index(min(arbre_probas))
        arbre_probas[min1] = temp
        
        if min1 > min2:
            min1, min2 = min2, min1
        for char in arbre_codes[min1]:
            codes[int(char)] = "0" + codes[int(char)]
        for char in arbre_codes[min2]:
            codes[int(char)] = "1" + codes[int(char)]
        nouvelle_proba = arbre_probas[min1] + arbre_probas[min2]
        nouveaux_codes = arbre_codes[min1] + arbre_codes[min2]
        
        arbre_probas.pop(min2)
        arbre_codes.pop(min2)
        arbre_probas.pop(min1)
        arbre_codes.pop(min1)
        arbre_probas.append(nouvelle_proba)
        arbre_codes.append(nouveaux_codes)
    return codes

def shannon_fano(probas):
    n = len(probas)
    probas_index = []
    for i in range(n):
        probas_index.append((probas[i], i))
    probas_index = sorted(probas_index, reverse=True)
    codes = [""] * n
    groupes = [[0, n-1]]
    while len(groupes) > 0:
        groupe = groupes.pop(0)
        debut = groupe[0]
        fin = groupe[1]
        if debut == fin:
            if codes[probas_index[debut][1]] == "":
                codes[probas_index[debut][1]] = "0"
            continue
        total = 0
        for i in range(debut, fin + 1):
            total = total + probas_index[i][0]
        
        somme = 0
        meilleur = debut
        diff_min = total
        
        for i in range(debut, fin):
            somme = somme + probas_index[i][0]
            diff = abs(somme - (total - somme))
            if diff < diff_min:
                diff_min = diff
                meilleur = i + 1
        
        for i in range(debut, meilleur):
            codes[probas_index[i][1]] = codes[probas_index[i][1]] + "0"
        for i in range(meilleur, fin + 1):
            codes[probas_index[i][1]] = codes[probas_index[i][1]] + "1"
        
        if meilleur - debut > 0:
            groupes.append([debut, meilleur - 1])
        if fin - meilleur + 1 > 0:
            groupes.append([meilleur, fin])
    return codes

def calcule(source, codes):
    ENT = 0
    for i in range(len(source)):
        if source[i] > 0:
            ENT +=(-source[i] * math.log2(source[i]))
    LONG = 0
    for j in range(len(codes)):
        LONG +=(source[j] * len(codes[j]))
    R =(ENT / LONG) if LONG > 0 else 0
    return ENT, LONG, R

print("PROGRAMME DE CODAGE DE SOURCE")


n = int(input("\nNombre de symboles : "))
probas = []
print(f"\nEntrez les {n} probabilités :")
for i in range(n):
    p = float(input(f"Probabilité du symbole {i} : "))
    probas.append(p)

print("\n--- PROBABILITÉS ENTRÉES ---")
for i in range(len(probas)):
    print(f"Symbole {i} : {probas[i]}")

print("\n--- MÉTHODE DE CODAGE ---")
print("1. Huffman")
print("2. Shannon-Fano")
choix = input("\nVotre choix (1 ou 2) : ")

if choix == "1":
    codes = huffman(probas)
    print("\n--- CODAGE DE HUFFMAN ---")
elif choix == "2":
    codes = shannon_fano(probas)
    print("\n--- CODAGE DE SHANNON-FANO ---")
else:
    print("NON monsieur KHALIL !")
    exit()

print("\nCodes générés :")
for i in range(len(codes)):
    print(f"Symbole {i} : {codes[i]}")

ENT, LONG, R = calcule(probas, codes)
print(f"Entropie           : {ENT:.2f} bits")
print(f"Longueur moyenne   : {LONG:.2f} bits")
print(f"efficacité         : {R:.2f} ({R*100:.2f}%)")
print("=" * 50)
