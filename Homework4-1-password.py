print("password Checker ")
password="algeria is great"
a=3
i=0
try:
    while a>i :
        User=input(" Write the password : ")
        if User == password:
            print("password correct")
            break
        else:
            print(" password not correct")
            i=i+1
except Exception as e:
    print(f"An unexpected error occurred: {e}")
   