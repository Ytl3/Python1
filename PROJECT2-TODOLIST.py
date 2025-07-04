import random
tasks=[]
def add_task ():
    ID=random.randint(1,999)
    nom=input("Nom de la tâche :").lower()
    desc =input("Description :").lower()
    stat=input("Statut (New/Completed) :").lower()
    tagg=input("Tag (High/Low) :").lower()
    task={'ID':ID,'Name':nom,'Description':desc,'Statut':stat,'Tag':tagg}
    tasks.append(task)
    print("Tâche ajoutée avec succès !")
    print(tasks)
    return task

def surch_task ():
    x=input("Entrer ID ou Nom de la tâche pour trouve la tache : ").lower()
    for task in tasks:
        if str(task['ID'])==x or task['Name'].lower()==x:
            print(task)
            return 
        print("no trouvable")

def delit_task ():
    Z=input("Entrer ID ou Nom de la tache pour suprime une tache : ").lower()
    for task in tasks:
        if str(task['ID'])==Z or task['Name'].lower()==Z:
            tasks.remove(task)
            print(tasks)
            return
        print("no trouvable")

def updat_task ():
    K=input("Entrer ID ou Nom de la tache pour change la statut  : ").lower()
    for task in tasks:
        if str(task['ID'])==K or task['Name'].lower()==K:
            w=input("Nouveau statut (New/completed)? : ")
            task['Statut']=w
            print(tasks)
            return
        print("no trouvable")

def lis_all ():
     print(" === liste des taches=== ")
     print(tasks)

def filtr_task ():
    O=input("Entrer statut ou vid : ").lower()
    y=input("Entrer Tag ou vid  : ").lower()
    for task in tasks:
        if str(task['Statut'])==O:
            print(tasks)
        elif task['Tag'].lower()==y:
            print(tasks)
        elif str(task['Statut'])==O and task['Tag'].lower()==y:
            print(tasks)
            return
        print("no trouvable")

def statistic_task():
    total = len(tasks)  
    new = 0
    completed = 0
    high = 0
    low = 0
    
    for task in tasks:
        if task['Statut'] == 'New':  
            new += 1
        elif task['Statut'] == 'Completed':  
            completed += 1
            
        if task['Tag'] == 'High': 
            high += 1
        elif task['Tag'] == 'Low': 
            low += 1
    
    print("=== Statistiques ===")
    print(f"Total: {total}")
    print(f"New: {new}")
    print(f"Completed: {completed}")
    print(f"High priority: {high}")
    print(f"Low priority: {low}")

def menu():
    while True:
        print("1- Ajouter une tâche ")
        print("2- Rechercher")
        print("3- Supprimer")
        print("4- Modifier statut")
        print("5-Lister tout")
        print("6- Filtrer")
        print("7- Statistiques")
        print("8- Quitter")
        Choice=input("number to choice or q to quit:")
        if Choice=="1":
         add_task()
        elif Choice=="2":
         surch_task()
        elif Choice=="3":
         delit_task()
        elif Choice=="4":
         updat_task()
        elif Choice=="5":
         lis_all()
        elif Choice=="6":
         filtr_task()
        elif Choice=="7":
         statistic_task()
        elif Choice=="q":
          print("THE END")  
          break
        else:
         print(" wath the fip brooo !!!")
      
     
menu()