import sys
import time
from datetime import datetime
import yaml

command_list = ["-h", "--help", "h", "help",
                "l", "t", "dd", "d", "a", "add", "e", "edit", "export"]


def showHelp():
    print("COMMANDS LIST")


def argsToDictionary(args):
    args_dict = {}
    for i in range(0, len(args), 2):
        if(not(command_list.__contains__(args[i]))):
            print("An argument isn't valid")
            exit()

        args_dict[args[i]] = args[i + 1]
    return args_dict


def verifyArg(arg):
    if(command_list.__contains__(arg)):
        return True
    return False


def containsHelp(key):
    if(
      (key == "-h") or
      (key == "--help") or
      (key == "h") or
      (key == "help")):
        return True

    return False


args = sys.argv
del args[0]

# COMMANDS

# Help

if(len(args) == 1 and args.__contains__("h")):
    showHelp()
    del args[args.index("h")]

if(len(args) == 1 and args.__contains__("help")):
    showHelp()
    del args[args.index("help")]

# List todolist

if(args.__contains__("l")):
    print("Showing todolist")
    del args[args.index("l")]

# List today todolist

if(args.__contains__("t")):
    print("Showing todolist for today")
    del args[args.index("l")]

# Delete done

if(args.__contains__("dd")):
    print("Delete done tasks")
    del args[args.index("dd")]

args_dict = argsToDictionary(args)
todos = []

if(args_dict.__contains__("a")):
    if(containsHelp(args_dict["a"])):
        print("""add "some task" """)
        exit()

    # after adding task ask for the date to done
    real_date = input('Enter a date in "MM/DD hh:mm" format : ')

    try:
        inp_date = datetime.strptime(real_date, "%m/%d %H:%M")
    except:
        print("Invalid date format")
        exit()

    actual_date = time.time()
    date = datetime(datetime.fromtimestamp(actual_date).year,
                    inp_date.month, inp_date.day, inp_date.hour, inp_date.minute)

    if(actual_date > date.timestamp()):
        next_year = datetime.fromtimestamp(actual_date).year + 1
        new_date = date.replace(year=next_year)
        todos.append({"date": new_date.timestamp(),
                      "content": args_dict["a"], "done": False})
    else:
        todos.append({"date": date.timestamp(),
                     "content": args_dict["a"], "done": False})


with open("output.yaml", "+a") as file:
    yaml.dump(yaml.safe_load(str(todos)), file)

with open("output.yaml", "r") as file:
    print(yaml.safe_load(file))
