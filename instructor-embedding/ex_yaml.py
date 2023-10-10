from ruamel.yaml import YAML
import sys

yaml = YAML(typ="unsafe")
# yaml.dump({"default":{"a":1,"b":2}}, sys.stdout)
out = yaml.load(open("test.yaml", "r"))

# print(yaml.dump(sys.stdout))
print(f"O: {out['default']}")
