class Student:

    #class variable
    school_name="Strathmore University"
    total_students=0
    def __init__(self, name, marks):
        self.name=name
        self.marks=marks
        Student.total_students+=1

    def greet(self):
        return f"Hi, I am {self.name}"

s1= Student("Jeremy",73)
s2= Student ("Madisson",83)

print (Student.total_students)

class BankAccount:
    def __init__(self,owner,balance):
        self.owner=owner
        self.__balance=balance

    def deposit(self, amount):
        if amount>0:
            self.__balance+=amount
        return amount
    def withdraw(self, amount):
        if amount>self.__balance:
            print("Can't withdraw, you have insufficient funds")
        self.__balance -= amount
        return amount

    def get_balance(self):
        return self.__balance
    
    

acc= BankAccount("Benir",1000)
print(acc.deposit(500))
print(acc.get_balance())
