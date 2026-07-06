def walls(cell_value) -> str:
    if (cell_value == 0):
        return " "  # Open
    elif (cell_value == 1):
        return "\u2578"  # North
    elif (cell_value == 2):
        return "\u2577"  # East
    elif (cell_value == 3):
        return "\u2514"  # North + East
    elif (cell_value == 4):
        return "\u2574"  # South
    elif (cell_value == 5):
        return "\u2502"  # South + North
    elif (cell_value == 6):
        return "\u250C"  # South + East
    elif (cell_value == 7):
        return "\u251C"  # South + North + East
    elif (cell_value == 8):
        return "\u2576"  # West
    elif (cell_value == 9):
        return "\u2518"  # West + North
    elif (cell_value == 10):
        return "\u2500"  # West + East
    elif (cell_value == 11):
        return "\u2534"  # West + North + East
    elif (cell_value == 12):
        return "\u2510"  # West + South
    elif (cell_value == 13):
        return "\u2524"  # West + South + North
    elif (cell_value == 14):
        return "\u252C"  # West + South + East
    elif (cell_value == 15):
        return "\u253C"  # West + South + North + East
    else:
        print("Wrong Cell Value")
        return "?"
# def walls(cell_value) -> str:
#     if (cell_value == 0):
#         return "0"  # Open
#     elif (cell_value == 1):
#         return "1"  # North
#     elif (cell_value == 2):
#         return "2"  # East
#     elif (cell_value == 3):
#         return "3"  # North + East
#     elif (cell_value == 4):
#         return "4"  # South
#     elif (cell_value == 5):
#         return "5"  # South + North
#     elif (cell_value == 6):
#         return "6"  # South + East
#     elif (cell_value == 7):
#         return "7"  # South + North + East
#     elif (cell_value == 8):
#         return "8"  # West
#     elif (cell_value == 9):
#         return "9"  # West + North
#     elif (cell_value == 10):
#         return "A"  # West + East
#     elif (cell_value == 11):
#         return "B"  # West + North + East
#     elif (cell_value == 12):
#         return "C"  # West + South
#     elif (cell_value == 13):
#         return "D"  # West + South + North
#     elif (cell_value == 14):
#         return "E"  # West + South + East
#     elif (cell_value == 15):
#         return "F"  # West + South + North + East
#     else:
#         print("Wrong Cell Value")
#         return "?"
