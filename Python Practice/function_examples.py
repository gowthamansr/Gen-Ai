# Basic Function Example
def greet():
    print("Hello, World!")

greet()

# Function with Parameters
def greet(name):
    print("Hello,", name)

greet("Arun")
greet("Priya")

#Function with Return Value
def add(a, b):
    return a + b

result = add(10, 20)
print(result)

#function with Default Parameters
def greet(name="Guest"):
    print("Welcome", name)

greet()
greet("Kumar")

# Function Returning Multiple Values
def calculations(a, b):
    return a + b, a - b

sum_value, diff_value = calculations(10, 5)

print(sum_value)
print(diff_value)