# Household Electricity Bill Calculator

def calculate_bill(units, late_payment):
    fixed_charge = 50

    # Electricity charge using slab rates
    if units <= 100:
        electricity_charge = units * 2

    elif units <= 200:
        electricity_charge = (100 * 2) + ((units - 100) * 3.50)

    else:
        electricity_charge = (100 * 2) + (100 * 3.50) + ((units - 200) * 5)

    # Late fee calculation
    if late_payment.upper() == "Y":
        late_fee = 0.05 * (electricity_charge + fixed_charge)
    else:
        late_fee = 0

    final_bill = electricity_charge + fixed_charge + late_fee

    return electricity_charge, fixed_charge, late_fee, final_bill


# Resident names already entered
resident_names = ["Param", "Parameshwar", "Navya Shree"]

# List to store all household details
households = []


# Input for all 3 residents
for name in resident_names:

    print("\nResident:", name)

    units = float(input("Enter units consumed: "))

    # Check for negative units
    while units < 0:
        print("Error: Units cannot be negative.")
        units = float(input("Enter units consumed again: "))

    late_payment = input("Is the payment late? (Y/N): ")

    electricity_charge, fixed_charge, late_fee, final_bill = calculate_bill(
        units, late_payment
    )

    household = {
        "name": name,
        "units": units,
        "electricity_charge": electricity_charge,
        "fixed_charge": fixed_charge,
        "late_fee": late_fee,
        "final_bill": final_bill
    }

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
    total_collection += household["final_bill"]


# Find resident with highest bill
highest_bill_household = households[0]

for household in households:
    if household["final_bill"] > highest_bill_household["final_bill"]:
        highest_bill_household = household


# Final summary
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