print("Temperature Logger")
temps=[]
try:
    while True:
        choice = input("Entrez une température (ou 'q' pour quitter) : ")
        if choice=='q':
            break
        else:
            temp=float(choice)
            print(f"votre temperature est {temp}°C")
        temps.append(temp)
        print(temps)
except Exception as e:
    print(e)
print("1 Nombre de relevé =", len(temps))
print("2 valeure maximale =",max(temps),". 2 la valeure minimale = ",min(temps), )
print("3 la moyenne = ",sum(temps)/len(temps),"arrondit a 1 decimal = ",round(sum(temps)/len(temps)))
    





























