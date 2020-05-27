# Pyaccessors: The key to lists

```python
list_of_dicts = [
    {"a": "A1", "b": 1},
    {"a": "A1", "b": 2},
    {"a": "A2", "b": 3},
]

accessor = access(list_of_dict, by="a", group=True)
print(accessor)
# {
#     "A1": [{"a": "A1", "b": 1}, {"a": "A1", "b": 2}],
#     "A2": [{"a": "A2", "b": 3},],
# }

```

