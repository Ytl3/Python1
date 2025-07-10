filename="grades.csv"
onefile="average.csv"
mode="r"
with open(onefile,"w")as k:
    k.write("names ;notes ;resulta\n")
    with open(filename,mode) as f:
        for line in f:
            data=line.strip().split(",")
            names=data[0]
            notes=[int(note) for note in data[1:]]
            average=sum(notes)/len(data[1:])
            print(names)
            print(notes)
            print(average)
            if average>=50:
                resulta=(data[0],average,"pass")
            else:
                resulta=(data[0],average,"Fail")
            k.write(f"{names}\n {notes}\n {average}\n {resulta}\n")

    

        















