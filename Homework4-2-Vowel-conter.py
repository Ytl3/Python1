print("Vowel Conter ")
User=input("Write what you want :").upper()
vowel="AEIOUY"
sum=0
for later in User:
    if later in vowel:
        sum=sum+1
print("the sum of the vowel =",sum)