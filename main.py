import sys
import time
from datetime import datetime
import inquirer
import yaml

# ARGS

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

# TODOS

todos = []

with open("output.yaml", "r") as file:
    try:
        file_load = yaml.safe_load(file)

        if(file_load):
            todos = file_load
    except:
        print("Invalid backup file content, deleting the file content")
        open('output.yaml', 'w').close()
        exit()


def todosContainContent(content):
    if(todos):
        for todo in todos:
            if(todo["content"] == content):
                return True

    return False


# Add todo

if(args_dict.__contains__("a")):
    content = args_dict["a"]

    if(containsHelp(content)):
        print("""add "some task" """)
        exit()

    if(todosContainContent(content)):
        print("This task already exists")
        answer = inquirer.prompt([inquirer.List(
            "continue", message="Would you like to continue ?", choices=["Yes", "No"])])

        if(answer["continue"] == "No"):
            exit()

    # after adding task ask for the date to done
    real_date = input('Enter a date in "MM/DD hh:mm" format : ')

    try:
        inp_date = datetime.strptime(real_date, "%m/%d %H:%M")
    except:
        print("Invalid date format")
        exit()

    actual_date = time.time()
    todo_date = datetime(datetime.fromtimestamp(actual_date).year,
                         inp_date.month, inp_date.day, inp_date.hour, inp_date.minute)

    if(actual_date > todo_date.timestamp()):
        next_year = datetime.fromtimestamp(actual_date).year + 1
        todo_date = todo_date.replace(year=next_year)

    todos.append({"date": todo_date.timestamp(),
                  "content": content, "done": False})

with open("output.yaml", "w+") as file:
    yaml.dump(yaml.safe_load(str(todos)), file)
