print("Slice Reporter")
data=list(range(1,21))
print(data)
print(data[:5])
print(data[15:])
print(data[::3])
print(data[::-1])
print("Even number filter function")
for num in data:
    if num & 1 == 0:
        print(num)


