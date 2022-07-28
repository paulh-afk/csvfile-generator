import yaml

content = """
  - date: 1659038646978
    content: "Practice Python"
    made: false

  - date: 1959038646978
    content: "Doing the dishes"
    made: true
"""

with open("output.yaml", "w") as file:
    yaml.dump(yaml.safe_load(content), file)

with open("output.yaml", "r") as file:
    print(yaml.safe_load(file))
