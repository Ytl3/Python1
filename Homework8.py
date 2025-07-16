class BankAccount:
    def __init__(self,owner,balance):
        self.owner=owner
        self.balance=balance
    def Deposit(self,amount):
        self.balance=self.balance + amount
        print(f"aprés avoir ajoute;{amount}$, on a balance ={self.balance}")
    def withdraw(self,amount):
        if self.balance >= amount:
            self.balance=self.balance - amount
            print(f" aprés avoir retiré;{amount}$ on a balance= {self.balance}")
        else :
            print("error")
compte1=BankAccount(input("donne votre nom :"),int(input("ajoute votre solde =")))
compte1.Deposit(int(input("ajoute votre montant =")))
compte2=BankAccount(input("donne votre nom :"),int(input("ajoute votre solde =")))
compte2.withdraw(int(input("ajoute votre montant=")))
compte3=BankAccount(input("donne votre nom :"),int(input("ajoute votre solde =")))
compte3.withdraw(int(input("ajoute votre montant=")))

print(f"the balance of {compte1.owner} is {compte1.balance}")
print(f"the balance of {compte2.owner} is {compte2.balance}")
print(f"the balance of {compte3.owner} is {compte3.balance}")