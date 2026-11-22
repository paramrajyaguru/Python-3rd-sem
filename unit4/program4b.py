while True:
    print("\n----- STUDENT DATA MANAGER -----")
    print("1. Add a new student record")
    print("2. Display all student records")
    print("3. Exit")
    
    choice = input("Enter your choice: ")
    
    if choice == "1":
        roll_no = input("Enter Roll Number: ")
        name = input("Enter Student Name: ")
        marks = input("Enter Marks: ")
        
        with open("students.txt", "a") as file:
            file.write(roll_no + "," + name + "," + marks + "\n")
            
        print("Student record added successfully!")
        
    elif choice == "2":
        try:
            with open("students.txt", "r") as file:
                print("\n----- STUDENT RECORDS -----")
                records = file.readlines()
                
                if len(records) == 0:
                    print("No student records found.")
                else:
                    for record in records:
                        roll_no, name, marks = record.strip().split(",")
                        print("Roll Number:", roll_no)
                        print("Student Name:", name)
                        print("Marks:", marks)
                        print("--------------------------")
                        
        except FileNotFoundError:
            print("No student records found. File does not exist.")
            
    elif choice == "3":
        print("Exiting the program...")
        break
        
    else:
        print("Invalid choice! Please try again.")