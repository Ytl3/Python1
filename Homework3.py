print ("the calculator")
print ("Entrer any two numbers you want ")
p1=float(input("Give the first number :"))
p2=float(input("Give the second number :"))
options=['+','-','*','/','%']
user=input('what type of equation do you want to do :').strip().lower()
if user == "+":
    print(f"addition de {p1} avec {p2} =",p1+p2 )
elif user=="-":
    print(f"subtractions de {p1} avec {p2} =",p1-p2 )
elif  user=="*":
    print(f"multiplication de {p1} avec {p2} =",p1*p2 )
elif  user=="/":
    if p2 != 0:
        print(f"division de {p1} avec {p2} =",p1/p2 )
    else:
        print ("Erreur")
elif  user=="%":
    if p2 != 0:
        print(f"modulo de {p1} avec {p2} =",p1%p2 )
    else:
        print ("Erreur")
else:
    print ('Opération non reconnue')
    