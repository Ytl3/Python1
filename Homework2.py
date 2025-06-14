#Rock paper scissor game using python 
print (" Le jeux est lancé :")   
Us1=input("Choisissez une des options suivant:Rock paper scissor;")
Us2=input("Choisissez une des options suivant:Rock paper scissor;")
if Us1==Us2:
    print ("égalité")
elif (Us1=="paper" and Us2=="rock") or (Us1=="scissor" and Us2=="paper" ) or (Us1=="rock" and Us2=="scissor" ):
    print("Us1 ; win the game ")
elif (Us1=="rock" and Us2=="paper") or (Us1=="paper" and Us2=="scissor" ) or (Us1=="scissor" and Us2=="rock" ):
    print("Us2 ; win the game")
else:
    print("redémarrer le jeux")