import math
#"Nom"="DJOUANI"
#"Prénom"="KHALIL"
#"Matricule"="222231481213"
print("1 - Quantité d'information  I(x)")
print("2 - Entropie                H(X)")
print("3 - Entropie conditionnelle H(X|Y)")
print("4 - Entropie conjointe      H(X,Y)")
print("5 - Information mutuelle    I(X;Y)")
print("=" * 40)
print("Entrez vos choix séparés par virgule")
print("Exemples :  1,2   ou   3,4,5   ou   1,2,3,4,5")
print("=" * 40)
choix_str = input("Votre choix : ").strip()
choix = [c.strip() for c in choix_str.split(",")]
def saisir_source(nom):
    n = int(input(f"Nombre de symboles de {nom} : "))
    source = {}
    for i in range(n):
        s = input(f"  Symbole {i+1} : ")
        p = float(input(f"  P({s}) = "))
        source[s] = p
    return source
def saisir_jointe():
    nX = int(input("Nombre de symboles de X : "))
    symbX = []
    for i in range(nX):
        s = input(f"  Symbole X{i+1} : ")
        symbX.append(s)
    nY = int(input("Nombre de symboles de Y : "))
    symbY = []
    for i in range(nY):
        s = input(f"  Symbole Y{i+1} : ")
        symbY.append(s)
    jointe = {}
    print(f"\nEntrez les {nX * nY} probabilités jointes :")
    for x in symbX:
        for y in symbY:
            p = float(input(f"  P(X={x}, Y={y}) = "))
            jointe[(x, y)] = p
    return jointe, symbX, symbY
def marginales(jointe, symbX, symbY):
    pX = {x: sum(jointe.get((x, y), 0) for y in symbY) for x in symbX}
    pY = {y: sum(jointe.get((x, y), 0) for x in symbX) for y in symbY}
    return pX, pY
besoin_jointe  = any(c in choix for c in ["3", "4", "5"])
besoin_source  = any(c in choix for c in ["1", "2"])
source = None
jointe = None
symbX  = None
symbY  = None
pX     = None
pY     = None
if besoin_jointe:
    jointe, symbX, symbY = saisir_jointe()
    pX, pY = marginales(jointe, symbX, symbY)
    source = pX
elif besoin_source:
    source = saisir_source("X")
print("\n" + "=" * 40)
print("           RÉSULTATS")
print("=" * 40)
# CALCUL 1 : I(x)
if "1" in choix:
    print("\n--- I(x) : Quantité d'information ---")
    for s, p in source.items():
        if p > 0:
            print(f"  I({s}) = -log2({p:.4f}) = {-math.log2(p):.4f} bits")
# CALCUL 2 : H(X)
if "2" in choix:
    H = -sum(p * math.log2(p) for p in source.values() if p > 0)
    print(f"\n--- H(X) : Entropie ---")
    print(f"  H(X) = {H:.6f} bits")
# CALCUL 3 : H(X|Y) et H(Y|X)
if "3" in choix:
    HXY = -sum(jointe[(x,y)] * math.log2(jointe[(x,y)] / pY[y])
               for x in symbX for y in symbY if jointe[(x,y)] > 0)
    HYX = -sum(jointe[(x,y)] * math.log2(jointe[(x,y)] / pX[x])
               for x in symbX for y in symbY if jointe[(x,y)] > 0)
    print(f"\n--- H(X|Y) : Entropie conditionnelle ---")
    print(f"  H(X|Y) = {HXY:.6f} bits")
    print(f"  H(Y|X) = {HYX:.6f} bits")
# CALCUL 4 : H(X,Y)
if "4" in choix:
    HconJ = -sum(p * math.log2(p) for p in jointe.values() if p > 0)
    print(f"\n--- H(X,Y) : Entropie conjointe ---")
    print(f"  H(X,Y) = {HconJ:.6f} bits")
# CALCUL 5 : I(X;Y)
if "5" in choix:
    hX  = -sum(p * math.log2(p) for p in pX.values() if p > 0)
    hY  = -sum(p * math.log2(p) for p in pY.values() if p > 0)
    hXY = -sum(p * math.log2(p) for p in jointe.values() if p > 0)
    iXY = hX + hY - hXY
    print(f"\n--- I(X;Y) : Information mutuelle ---")
    print(f"  H(X)   = {hX:.6f} bits")
    print(f"  H(Y)   = {hY:.6f} bits")
    print(f"  H(X,Y) = {hXY:.6f} bits")
    print(f"  I(X;Y) = {iXY:.6f} bits")
print("\n" + "=" * 40)
print("Calculs terminés.")