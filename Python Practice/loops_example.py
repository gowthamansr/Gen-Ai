# For Loop
for i in range(5):
    print("Iteration:", i)

fruits = ["apple", "banana", "mango"]
for fruit in fruits:
    print("Fruit:", fruit)

total = 0

for i in range(1, 6):
    total += i

print("Total:", total)

# While Loop
xtotal = 0

for i in range(1, 6):
    xtotal += i

print("Total:", xtotal)

n = 5

while n > 0:
    print(n)
    n -= 1

print("Done!")

# Nested Loops
for i in range(1, 4):
    for j in range(1, 4):
        print(i, "*", j, "=", i * j)

# Loop Control Statements
for i in range(1, 10):
    if i == 5:
        break
    print(i)

#Find Even Numbers
numbers = [1, 2, 3, 4, 5, 6]

for n in numbers:
    if n % 2 == 0:
        print(n)