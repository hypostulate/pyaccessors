from collections import defaultdict
from functools import lru_cache
from typing import (
    List,
    Dict,
    Optional,
    Any,
    Union,
    Tuple,
)


# Type definitions
JsonObject = Dict[str, Any]
JsonList = List[JsonObject]
JsonInput = Union[JsonList, JsonObject]
ListAccessor = Dict[Union[str, int, float, bool], JsonList]
DictAccessor = Dict[Union[str, int, float, bool], JsonObject]


def access(
    obj: JsonInput,
    by: Union[str, List[str], Tuple[str]],
    strict: bool = False,
    group: bool = False,
) -> Union[DictAccessor, ListAccessor]:
    """Restructures a json-like datastructure as a dictionary where
    the values accessed by `keys` are the dict keys and the underlying objects are the values
    
    Parameters
    ----------
    obj : JsonInput
        A valid Json object (dict or list) 
    *keys : str
        The keys to access with the values of. Multiple keys specified will dig "deeper"
        into the dict objects.
    strict : bool
        Whether all items must have the key
    group : bool
        Whether to group identical values together in lists. If false, a ValueError is raised
        if identical values are found. 

    Returns
    -------
    JsonObject
        A JsonObject dictionary for access by values of `key`.
    
    Raises
    ------
    ValueError
        If `key` values are not unique and `group` == False
    """
    if isinstance(by, str):
        keys = [by]
    elif isinstance(by, (list, tuple)):
        keys = by
    else:
        raise TypeError(f"'by' must be str, list, or tuple not {type(by)}")

    if not isinstance(strict, bool):
        raise TypeError(
            f"Argument 'strict' invalid type '{type(strict)}' expected bool"
        )

    accessible: Union[DictAccessor, ListAccessor]
    if group:
        accessible = _group_access(obj, *keys, strict=strict)
    else:
        accessible = _individual_access(obj, *keys, strict=strict)
    return accessible


def _group_access(obj: JsonInput, *keys: str, strict: bool = False) -> ListAccessor:
    """Creates a dict of lists structure"""
    accessible = defaultdict(list)
    for item in _cast_to_list(obj):
        if strict:
            val = _strict_get_value(item, *keys)
        else:
            val = _loose_get_value(item, *keys)
        if val:
            accessible[val].append(item)
    return accessible


def _individual_access(
    obj: JsonInput, *keys: str, strict: bool = False
) -> DictAccessor:
    """Creates a dict of objects structure"""
    accessible = {}
    for item in _cast_to_list(obj):
        if strict:
            val = _strict_get_value(item, *keys)
        else:
            val = _loose_get_value(item, *keys)
        if isinstance(val, (str, int, float)) and val in accessible:
            raise ValueError(
                f"Multiple items contain value: '{val}'. Try 'group=True'."
            )
        elif val:
            accessible[val] = item
    return accessible


def _strict_get_value(item: JsonObject, *keys: str) -> Any:
    """Wrap KeyError for more explanation"""
    try:
        val = item
        for key in keys:
            if isinstance(val, dict):
                val = val[key]
            else:
                raise KeyError(f"Access path {keys} leads to a non-dict object.")
    except KeyError:
        raise KeyError(f"Key '{keys}' does not exist in all items. Try 'strict=False'.")
    else:
        return val


def _loose_get_value(item: JsonObject, *keys: str) -> Any:
    val = item
    for key in keys:
        if isinstance(val, dict):
            val = val.get(key, {})
        else:
            val = {}
    return val


def _cast_to_list(obj: JsonInput) -> JsonList:
    """Ensures the object is properly encapsulated as a list of Json objects"""
    if isinstance(obj, list):
        return obj
    elif isinstance(obj, dict):
        return [obj]
    else:
        raise ValueError("Object is not a list of dict")
