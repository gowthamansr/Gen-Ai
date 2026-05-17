# Creating a Dictionary
student = {
    "name": "Arun",
    "age": 21,
    "course": "Python"
}

print(student)

# Accessing Values
print("Name:", student["name"])
print("Age:", student["age"])
print("Course:", student["course"])

# Adding and Modifying Values
student["age"] = 22
print("Updated Age:", student["age"])

student["grade"] = "A"
print("Grade:", student["grade"])

#Removing Items
del student["course"]
print(student)

#check if key exists
if "name" in student:
    print("Key exists")