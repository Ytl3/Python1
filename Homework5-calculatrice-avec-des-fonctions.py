import math 

def add(a,b):
    return a+b
def soustraction(a,b):
    return a-b
def multiplication(a,b):
    return a*b
def division(a,b):    
    if b==0:
        return "Erreur : b!=0"
    return a/b
def modulo(a,b):
    if b==0:
        return "Erreur : b!=0"
    return a%b
def puissance(a,b):
    return a**b
def racine_carre(a):
    if a<0:
        return "Erreur : a!=0"
    return math.sqrt(a)
def calculatrice():
    print(" calculator ")
    print("Please choose an operation:")
    print("1:+")
    print("2:-")
    print("3:*")
    print("4:/")
    print("5:%")
    print("6:**")
    print("7:sqrt")
    print("8:quit")


calculatrice()
a=float(input("Give the first number :"))
b=float(input("Give the second number :"))

while True:
    choice=int(input("please enter a number between 1 and 8 :"))
    if choice==str():
        print(input("I beg you enter a number between 1 and 8"))
        choice=int(input("please enter a number between 1 and 8"))
    if choice==8:
        print("end")
        break
    elif choice==7:
        print(f"le recine carre de {a} =",racine_carre(a))
    elif choice==6:
        print(f"la puussance de {a} avec {b} =",puissance(a, b))
    elif choice==5:
        print(f"le modulo de {a} avec {b} =",modulo(a, b))
    elif choice==4:
        print(f"la division entre {a} est {b} =",division(a, b))
    elif choice==3:
        print(f"la multiplication entre {a} esr {b} =",multiplication(a, b))
    elif choice==2:
        print(f"la soustraction entre {a} esr {b} =",soustraction(a, b))
    elif choice==1:
        print(f"la addition entre {a} esr {b} =",add(a, b))

    
         
    