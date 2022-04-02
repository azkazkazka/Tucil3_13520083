from solver import matrixInput, matrixFile, reachable, getIdx, search


print("\n▄█ █▀   █▀█ █░█ ▀█ ▀█ █░░ █▀▀   █▀ █▀█ █░░ █░█ █▀▀ █▀█")
print("░█ ▄█   █▀▀ █▄█ █▄ █▄ █▄▄ ██▄   ▄█ █▄█ █▄▄ ▀▄▀ ██▄ █▀▄\n")

print("----------------------------------------------------------\n")
print("PILIHAN INPUT PUZZLE")
print("1. Input Manual")
print("2. Input File")

choice = int(input("Pilih input puzzle: "))

while(choice != 1 and choice != 2):
    # invalid input
    print("Pilihan tidak tersedia. Coba lagi")

print("\n----------------------------------------------------------\n")
print("INPUT PUZZLE")
if (choice == 1):  
    # input user
    puzzle, blank, lowerbound = matrixInput()
else:
    # input file
    string = input("Enter nama file: ")
    puzzle, blank, lowerbound = matrixFile(string)

print("\n----------------------------------------------------------\n")
# the rest of the file
x, y = getIdx(puzzle, blank)
reachability = reachable(puzzle, blank, x, y)
print("\n----------------------------------------------------------\n")

if (reachability):
    search(puzzle, blank, lowerbound)
else:
    print("PUZZLE UNREACHABLE!")
 