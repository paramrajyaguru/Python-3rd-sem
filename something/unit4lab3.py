# Lab Exercise 3: CSV-Based Payroll Management System

import csv

try:
    n = int(input("Enter number of employees: "))

    # Create and write CSV file
    with open("payroll.csv", "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(["Employee ID", "Name", "Basic Salary",
                         "Allowance", "Deduction", "Net Salary"])

        for i in range(n):
            print("\nEnter details of Employee", i + 1)

            emp_id = input("Enter Employee ID: ")
            name = input("Enter Name: ")
            basic = float(input("Enter Basic Salary: "))
            allowance = float(input("Enter Allowance: "))
            deduction = float(input("Enter Deduction: "))

            net_salary = basic + allowance - deduction

            writer.writerow([emp_id, name, basic,
                             allowance, deduction, net_salary])

    print("\nPayroll records saved successfully!")

    # Read and display CSV file
    print("\nEmployee Payroll Records:")
    print("--------------------------------")

    with open("payroll.csv", "r") as file:
        reader = csv.reader(file)

        for row in reader:
            print(" | ".join(row))

except ValueError:
    print("Please enter valid numeric values!")