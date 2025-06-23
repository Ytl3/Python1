print("FACT")
Number=int(input("give me a number not a str :"))
sum=Number
for i in range(1,Number):
    print(sum*i)
    sum=sum*i
print(f"the fact of {Number} is :",sum)
    
