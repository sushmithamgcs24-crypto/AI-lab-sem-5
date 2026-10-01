# Vacuum Cleaner Agent - 2 Rooms

# Read the status of Room A and Room B
room_A = input("Enter status of Room A (CLEAN/DIRTY): ").upper()
room_B = input("Enter status of Room B (CLEAN/DIRTY): ").upper()

# Read initial location of vacuum
location = input("Enter initial location of vacuum (A/B): ").upper()

print("\n--- Vacuum Cleaner Process ---")

# Repeat until both rooms are clean
while room_A != "CLEAN" or room_B != "CLEAN":

    # If vacuum is in Room A
    if location == "A":

        if room_A == "DIRTY":
            print("Vacuum is in Room A")
            print("Action: Clean Room A")
            room_A = "CLEAN"

        else:
            print("Room A is already CLEAN")
            print("Action: Move to Room B")
            location = "B"

    # If vacuum is in Room B
    elif location == "B":

        if room_B == "DIRTY":
            print("Vacuum is in Room B")
            print("Action: Clean Room B")
            room_B = "CLEAN"

        else:
            print("Room B is already CLEAN")
            print("Action: Move to Room A")
            location = "A"


# Display final status
print("\n--- Final Status ---")
print("Room A =", room_A)
print("Room B =", room_B)

print("\nGoal Achieved! Both rooms are CLEAN.")