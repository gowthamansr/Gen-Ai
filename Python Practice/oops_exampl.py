# Class Object 
class Student:
    pass

s1 = Student()

print(type(s1))

# Class with Attributes
class Student:
    name = "Arun"
    age = 21

s1 = Student()

print(s1.name)
print(s1.age)

#Constructor (__init__)
class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

s1 = Student("Arun", 21)

print(s1.name)
print(s1.age)

# Instance Methods
class Student:
    def __init__(self, name):
        self.name = name

    def greet(self):
        print("Hello", self.name)

s1 = Student("Arun")

s1.greet()

#self Keyword
class Car:
    def show(self):
        print("This is a car")

c1 = Car()

c1.show()

#Multiple Objects
class Student:
    def __init__(self, name):
        self.name = name

s1 = Student("Arun")
s2 = Student("Priya")

print(s1.name)
print(s2.name)

#Inheritance
class Animal:
    def sound(self):
        print("Animal makes sound")

class Dog(Animal):
    pass

d = Dog()

d.sound()

#Encapsulation
class Bank:
    def __init__(self):
        self.__balance = 1000

    def show_balance(self):
        print(self.__balance)

b = Bank()

b.show_balance()

#Polymorphism
class Cat:
    def sound(self):
        print("Meow")

class Dog:
    def sound(self):
        print("Bark")

animals = [Cat(), Dog()]

for animal in animals:
    animal.sound()

#Abstraction
from abc import ABC, abstractmethod

class Vehicle(ABC):

    @abstractmethod
    def start(self):
        pass

class Car(Vehicle):

    def start(self):
        print("Car starts")

c = Car()

c.start()