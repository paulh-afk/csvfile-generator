import sys
import time
import yaml


def showHelp():
    print("COMMANDS LIST")


def argsToDictionary(args):
    result = {}
    for i in range(0, len(args), 2):
        result[args[i]] = args[i + 1]
    return result


args = sys.argv
del args[0]

# COMMANDS

# Help

if(args.__contains__("-h")):
    showHelp()
    del args[args.index("-h")]

if(args.__contains__("--help")):
    showHelp()
    del args[args.index("--help")]

if(args.__contains__("h")):
    showHelp()
    del args[args.index("h")]

if(args.__contains__("help")):
    showHelp()
    del args[args.index("help")]

# List todolist

if(args.__contains__("-l")):
    print("Showing todolist")
    del args[args.index("-l")]

# List today todolist

if(args.__contains__("-t")):
    print("Showing todolist for today")
    del args[args.index("-l")]

# Delete done

if(args.__contains__("-dd")):
    print("Delete done tasks")
    del args[args.index("-dd")]

print(argsToDictionary(args))

# print(time.time())
# after adding task ask for the date to done

content = """
  - date: 1659038646978
    content: "Practice Python"
    done: false

  - date: 1959038646978
    content: "Doing the dishes"
    done: true
"""

with open("output.yaml", "w") as file:
    yaml.dump(yaml.safe_load(content), file)

with open("output.yaml", "r") as file:
    print(yaml.safe_load(file))
