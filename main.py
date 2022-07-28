import yaml

content = """
1:
  - 1659038646978
  - "Practice Python"
  - false
2:
  - 1959038646978
  - "Doing the dishes"
  - true
""" 

with open("output.yaml", "w") as file:
    yaml.dump(yaml.safe_load(content), file)

with open("output.yaml", "r") as file:
    print(yaml.safe_load(file))
