# Pyaccessors: The key to lists

## Install

`pip install pyaccessors`

## Usage

### Unique Access
```python
from pyaccessors import access

list_of_dicts = [
    {"a": "A1", "b": 1},
    {"a": "A2", "b": 2},
    {"a": "A3", "b": 3},
]

accessor = access(list_of_dict, by="a")

# if you want to fail when the key does not exist
# accessor = access(list_of_dict, by="a", strict=True)

print(accessor)
# {
#     "A1": {"a": "A1", "b": 1}, 
#     "A2": {"a": "A2", "b": 2},
#     "A3": {"a": "A3", "b": 3},
# }
```

### Grouped Access
```python
from pyaccessors import access

list_of_dicts = [
    {"a": "A1", "b": 1},
    {"a": "A1", "b": 2},
    {"a": "A2", "b": 3},
]

accessor = access(list_of_dict, by="a", group=True)
print(accessor)
# {
#     "A1": [{"a": "A1", "b": 1}, {"a": "A1", "b": 2}],
#     "A2": [{"a": "A2", "b": 3}],
# }
```

### Deep Access
```python
from pyaccessors import access

list_of_dicts = [
    {"a": "A1", "b": {"c": 1}},
    {"a": "A1", "b": {"c": 2}},
    {"a": "A2", "b": {"c": 3}},
]

accessor = access(list_of_dict, by=["b", "c"])
print(accessor)
# {
#     1: {"a": "A1", "b": {"c": 1}},
#     2: {"a": "A1", "b": {"c": 2}},
#     3: {"a": "A2", "b": {"c": 3}},
# }
```

