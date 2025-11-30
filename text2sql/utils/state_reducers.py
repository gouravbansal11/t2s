"""
State Reducer Utilities for LangGraph

This module provides reducer functions for handling concurrent state updates
in LangGraph StateGraph definitions. These reducers are used with Annotated
types to automatically merge updates from concurrent nodes.
"""

def merge_dicts(left: dict, right: dict) -> dict:
    """
    Merge two dictionaries with right values taking precedence over left values.
    
    This reducer is used for state fields that need to be updated by multiple
    concurrent nodes. It combines updates without conflicts.
    
    Args:
        left (dict): The current state dictionary
        right (dict): The update dictionary from a node
    
    Returns:
        dict: Merged dictionary with updates applied
    
    Example:
        >>> current = {"agent1": [1, 2], "agent2": [3]}
        >>> update = {"agent3": [4, 5]}
        >>> merge_dicts(current, update)
        {"agent1": [1, 2], "agent2": [3], "agent3": [4, 5]}
    
    Usage in StateGraph:
        from typing import Annotated
        from pydantic import BaseModel
        from utils.stateReducers import merge_dicts
        
        class MyState(BaseModel):
            agent_results: Annotated[dict, merge_dicts] = {}
        
        # Now multiple nodes can update agent_results concurrently
        # without conflicts
    """
    result = dict(left) if left else {}
    if right:
        result.update(right)
    return result


def merge_lists(left: list, right: list) -> list:
    """
    Merge two lists by extending the left list with right list items.
    
    This reducer is used for state fields that accumulate values from multiple
    concurrent nodes.
    
    Args:
        left (list): The current state list
        right (list): The items to add from a node
    
    Returns:
        list: Combined list with items from both left and right
    
    Example:
        >>> current = [1, 2, 3]
        >>> update = [4, 5]
        >>> merge_lists(current, update)
        [1, 2, 3, 4, 5]
    
    Usage in StateGraph:
        from typing import Annotated
        from pydantic import BaseModel
        from utils.stateReducers import merge_lists
        
        class MyState(BaseModel):
            all_results: Annotated[list, merge_lists] = []
        
        # Multiple nodes can append to all_results concurrently
    """
    result = list(left) if left else []
    if right:
        result.extend(right)
    return result


def keep_last(left: any, right: any) -> any:
    """
    Keep the rightmost (most recent) value, discarding the previous value.
    
    This reducer is used when you want the latest value to override any previous
    value, typically for scalar or atomic values.
    
    Args:
        left (any): The previous value
        right (any): The new value
    
    Returns:
        any: The new value (right parameter)
    
    Example:
        >>> keep_last("old_query", "new_query")
        "new_query"
    
    Usage in StateGraph:
        from typing import Annotated
        from pydantic import BaseModel
        from utils.stateReducers import keep_last
        
        class MyState(BaseModel):
            latest_result: Annotated[str, keep_last] = ""
    """
    return right if right is not None else left


def merge_sets(left: set, right: set) -> set:
    """
    Merge two sets by taking their union.
    
    This reducer is used for state fields that represent unique collections
    updated by multiple concurrent nodes.
    
    Args:
        left (set): The current state set
        right (set): Items to add from a node
    
    Returns:
        set: Union of both sets
    
    Example:
        >>> current = {1, 2, 3}
        >>> update = {3, 4, 5}
        >>> merge_sets(current, update)
        {1, 2, 3, 4, 5}
    
    Usage in StateGraph:
        from typing import Annotated
        from pydantic import BaseModel
        from utils.stateReducers import merge_sets
        
        class MyState(BaseModel):
            unique_items: Annotated[set, merge_sets] = set()
    """
    left_set = set(left) if left else set()
    right_set = set(right) if right else set()
    return left_set.union(right_set)
