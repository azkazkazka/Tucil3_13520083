from solver import matrixInput, matrixFile, reachable, getIdx, search

print("\n▄█ █▀   █▀█ █░█ ▀█ ▀█ █░░ █▀▀   █▀ █▀█ █░░ █░█ █▀▀ █▀█")
print("░█ ▄█   █▀▀ █▄█ █▄ █▄ █▄▄ ██▄   ▄█ █▄█ █▄▄ ▀▄▀ ██▄ █▀▄\n")

print("----------------------------------------------------------\n")
print("PILIHAN INPUT PUZZLE")
print("1. Input Manual")
print("2. Input File")
choice = int(input("Pilih input puzzle: "))
# invalid input
while(choice != 1 and choice != 2):
    print("Pilihan tidak tersedia. Coba lagi")
print("\n----------------------------------------------------------\n")
print("INPUT PUZZLE")
# input user
if (choice == 1):  
    puzzle, blank, lowerbound = matrixInput()
# input file
else:
    string = input("Enter nama file: ")
    puzzle, blank, lowerbound = matrixFile(string)
print("\n----------------------------------------------------------\n")
# check reachability
x, y = getIdx(puzzle, blank)
reachability = reachable(puzzle, blank, x, y)
print("\n----------------------------------------------------------\n")
# search
if (reachability):
    search(puzzle, blank, lowerbound)
else:
    print("PUZZLE UNREACHABLE!")
 