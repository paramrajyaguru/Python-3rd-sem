try:
    # Open the log file in read mode
    with open("log.txt", "r") as file:

        error_count = 0

        print("Log File Contents:")
        print("------------------")
        line=file.readline()
        # Read and display the file line by line
        while line:
            print(line.strip())
 
            # Count ERROR messages
            if "ERROR" in line:
                error_count += 1
            line=file.readline()
        # Display total number of errors
        print("\nTotal number of ERROR messages:", error_count)

except FileNotFoundError:
    print("log.txt file does not exist.")