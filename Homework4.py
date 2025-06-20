print(" Sum of the first N numbers")
try:
    N=float(input("donne un nombre ; "))
    sum=0
    for i in range(1,N+1): 
        sum=sum+i
    print("la somme de les premie nombre de N est = ", sum)
except Exception as e:
    print(f"An unexpected error occurred: {e}")
