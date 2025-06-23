print("Number is prime ")
Number=int(input("give me a number not a str :"))
if Number<=1:
    print("number no prime")
else:
    for i in range(2,Number):
        div=Number%i
        if div ==0:
            print("no prime")
            break
        elif div!=0:
            print(Number,"is prime number")
            break
