p = []

for i in range(5):
    bt = int(input(f"Enter burst time for P{i+1}: "))
    p.append([i+1, bt])

p.sort(key=lambda x: x[1])

wt = 0

print("\nProcess\tBT\tWT\tTAT")

for pid, bt in p:
    tat = wt + bt
    print(f"P{pid}\t{bt}\t{wt}\t{tat}")
    wt += bt