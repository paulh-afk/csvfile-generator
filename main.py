import sys
import time
from datetime import datetime
import inquirer
import yaml

command_list = ["-h", "--help", "h", "help",
                "l", "list", "t",
                "c", "count",
                "dd", "del", "delete",
                "a", "add",
                "d", "done",
                "e", "edit",
                "export"]


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


def singleContainsHelp():
    if(
      (args.__contains__("-h")) or
      (args.__contains__("--help")) or
      (args.__contains__("h")) or
      (args.__contains__("help"))):
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


def minutesConverter(minutes):
    if(minutes < 10):
        return "0" + str(minutes)

    return minutes


# Delete program name from args
args = sys.argv
del args[0]

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


def sortTodos():
    for _ in range(len(todos) - 1):
        for j in range(len(todos) - 1):
            if(todos[j]["date"] > todos[j + 1]["date"]):
                greatest = todos[j]
                todos[j] = todos[j + 1]
                todos[j + 1] = greatest


# COMMANDS
# Help

if(len(args) == 1 and args.__contains__("h")):
    showHelp()
    del args[args.index("h")]

if(len(args) == 1 and args.__contains__("help")):
    showHelp()
    del args[args.index("help")]

# Count todos


def printCountTodos():
    print("There is", str(len(todos)), "task todo !")


if(args.__contains__("c")):
    del args[args.index("c")]

    if(singleContainsHelp()):
        print("Return nomber of todos")
        exit()

    printCountTodos()

if(args.__contains__("count")):
    del args[args.index("count")]

    if(singleContainsHelp()):
        print("Return nomber of todos")
        exit()

    printCountTodos()

# List todolist


def showTodos():
    if(len(todos) == 0):
        print("No tasks !")

    for todo in todos:
        date = datetime.fromtimestamp(todo["date"])
        minutes = minutesConverter(date.minute)
        print(date.month, "-", date.day, " / ", date.hour,
              ":", minutes, " | ", todo["content"], sep="")


if(args.__contains__("l")):
    del args[args.index("l")]
    showTodos()

if(args.__contains__("list")):
    del args[args.index("list")]
    showTodos()


# List today todolist

if(args.__contains__("t")):
    del args[args.index("t")]

    if(singleContainsHelp()):
        print("Delete done tasks")
        exit()

    for todo in todos:
        actual_ts = time.time()

        print(actual_ts)

    # get actual date 00:00 to 23:59 todos


# Delete done todos

if(args.__contains__("dd")):
    del args[args.index("dd")]

    if(singleContainsHelp()):
        print("Delete done tasks")
        exit()

    not_done_todos = list()

    for todo in todos:
        if(not(todo["done"])):
            not_done_todos.append(todo)

    todos = not_done_todos

try:
    args_dict = argsToDictionary(args)
except:
    print("An argument isn't valid")
    exit()


# Delete todo


def deleteTodo(content):
    global todos

    if(content == "*"):
        todos.clear()
        exit()

    content_index = int
    try:
        content_index = int(content)
    except:
        content_index = None

    if(content_index != None):
        # index
        try:
            todos.pop(content_index)
        except:
            exit()
    else:
        # content
        not_deleted_todos = list()

        for todo in todos:
            if(todo["content"] != content):
                not_deleted_todos.append(todo)

        todos = not_deleted_todos


if(args.__contains__("del")):
    content = args_dict["del"]

    if(containsHelp(content)):
        print("""del <index|content>""")
        exit()

    deleteTodo(content)


if(args.__contains__("delete")):
    content = args_dict["delete"]

    if(containsHelp(content)):
        print("""delete <index|content>""")
        exit()

    deleteTodo(content)


# Add todo


def addTodo(content):
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

    answer = inquirer.prompt([inquirer.List(
        "again", message="Do you want to add another task ?", choices=["Yes", "No"])])
    if(answer["again"] == "Yes"):
        content = input("Enter the task name : ")
        addTodo(content)


if(args_dict.__contains__("a")):
    content = args_dict["a"]

    if(containsHelp(content)):
        print("""a "some task" """)
        exit()

    addTodo(content)

if(args_dict.__contains__("add")):
    content = args_dict["add"]

    if(containsHelp(content)):
        print("""add "some task" """)
        exit()

    addTodo(content)

# Done Todo
# param: index or todo content


def doneTodo(content):
    index = int
    try:
        index = int(content)
    except:
        index = None

    if(index != None):
        # index
        try:
            todos[index]["done"] = True
        except:
            exit()
    else:
        # content
        for todo in todos:
            if(todo["content"] == content):
                todo["done"] = True


if(args_dict.__contains__("d")):
    content = args_dict["d"]

    if(containsHelp(content)):
        print("""d <index|content>""")
        exit()

    doneTodo(content)

if(args_dict.__contains__("done")):
    content = args_dict["done"]

    if(containsHelp(content)):
        print("""done <index|content>""")
        exit()

    doneTodo(content)

# Edit todo


def editTodo(inp_data):
    index = None
    content = str()

    try:
        index = int(inp_data)
        content = todos[index]["content"]
    except:
        index = None

    for i in range(len(todos)):
        if(todos[i]["content"] == inp_data):
            content = todos[i]["content"]
            index = i

    if(index == None):
        exit()

    new_content = input('The content was ' + content +
                        ", what would you replace it with ? ")

    todos[index]["content"] = new_content


if(args_dict.__contains__("e")):
    content = args_dict["e"]

    if(containsHelp(content)):
        print("""e <index|content>""")
        exit()

    editTodo(content)


if(args_dict.__contains__("edit")):
    content = args_dict["edit"]

    if(containsHelp(content)):
        print("""edit <index|content>""")
        exit()

    editTodo(content)


sortTodos()

with open("output.yaml", "w+") as file:
    yaml.dump(yaml.safe_load(str(todos)), file)
