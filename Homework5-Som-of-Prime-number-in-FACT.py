def est_prime(X):
    if X<=1:
       return False
    else:
        for i in range(2,X):
             if X%i ==0:
               return False
        return True
    
n = int(input("Entrez un nombre : "))
somme = 0

for i in range(1,n+1):
    if est_prime(i):
        somme += i

print(f"La somme des nombres premiers jusqu'à {n} est : {somme}")