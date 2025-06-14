#Ask user to give two values,and print their sum
a=float(input("donnez un chiffre  ;"))
b=float(input("donnez un chiffre  ;"))
c=a+b
print("La sum est=",c)

#Ask user for their birthyear, and print their age
while True:
     naissance=input("donne votre date de naissance : ")
     if naissance.isdigit():
         naissance=int(naissance)
         break
     else:
         print("erreur entre votre vair date de naissance")
annee=int(input("entre l'annéé actuelle : "))
if annee >= naissance:
     print("vous avez ",annee-naissance,"ans" )
else:
     print( "erreur entre votre vair date de naissance")

