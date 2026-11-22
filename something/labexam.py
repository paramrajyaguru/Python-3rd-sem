# Household Electricity Bill Calculator

# Function to calculate bill for one household
def calculate_bill(units, late_payment):
    fixed_charge = 50

    # Calculate electricity charge according to slabs
    if units <= 100:
        electricity_charge = units * 2

    elif units <= 200:
        electricity_charge = (100 * 2) + ((units - 100) * 3.50)

    else:
        electricity_charge = (100 * 2) + (100 * 3.50) + ((units - 200) * 5)

    # Calculate late fee
    if late_payment.upper() == "Y":
        late_fee = 0.05 * (electricity_charge + fixed_charge)
    else:
        late_fee = 0

    # Calculate final bill
    final_bill = electricity_charge + fixed_charge + late_fee

    return electricity_charge, fixed_charge, late_fee, final_bill


# List to store details of all households
households = []


# Take input for 3 households
for i in range(3):

    print("\nHousehold", i + 1)

    name = input("Enter resident's name: ")

    units = float(input("Enter units consumed: "))

    # Reject negative units
    while units < 0:
        print("Error: Units cannot be negative.")
        units = float(input("Enter units consumed again: "))

    late_payment = input("Is the payment late? (Y/N): ")

    # Calculate the bill
    electricity_charge, fixed_charge, late_fee, final_bill = calculate_bill(
        units, late_payment
    )

    # Store household details in a dictionary
    household = {
        "name": name,
        "units": units,
        "electricity_charge": electricity_charge,
        "fixed_charge": fixed_charge,
        "late_fee": late_fee,
        "final_bill": final_bill
    }

    # Add dictionary to the list
    households.append(household)


# Display bill details
print("\n========== ELECTRICITY BILL DETAILS ==========")

for household in households:

    print("\nResident Name:", household["name"])
    print("Units Consumed:", household["units"])
    print("Electricity Charge: ₹", round(household["electricity_charge"], 2))
    print("Fixed Charge: ₹", round(household["fixed_charge"], 2))
    print("Late Fee: ₹", round(household["late_fee"], 2))
    print("Final Bill Amount: ₹", round(household["final_bill"], 2))


# Calculate total collection
total_collection = 0

for household in households:
    total_collection = total_collection + household["final_bill"]


# Find household with highest bill
highest_bill_household = households[0]

for household in households:
    if household["final_bill"] > highest_bill_household["final_bill"]:
        highest_bill_household = household


# Display final results
print("\n========== FINAL SUMMARY ==========")

print("Total Collection: ₹", round(total_collection, 2))

print(
    "Resident with Highest Bill:",
    highest_bill_household["name"]
)

print(
    "Highest Bill Amount: ₹",
    round(highest_bill_household["final_bill"], 2)
)