#!/usr/bin/env python
# -*- coding: utf-8 -*-
from inspect import isfunction
from test_runner.expect import NoExpectException

def do_assertion(action, actual, expect, message = ""):
    # 0 - Success, 1 - Failure, -1 - Error
    ret = {"result": 1, "detail": None, "message": message, "actual": actual, "expect": expect}
    try:
        ret["result"] = 0 if _do_assertion(action, actual, expect) else 1
    except Exception, e:
        ret["result"] = -1
        ret["detail"] = e
    return ret

def _do_assertion(action, actual, expect):
    ret = False
    if isfunction(actual):
        actual = actual()
        
    if "ok" == action:
        ret = _take_action("equal", actual, True)
    elif "not_ok" == action:
        ret = _take_action("equal", actual, False)
    elif "equal" == action:
        ret = _take_action("equal", actual, expect)
    elif "not_equal" == action:
        ret = _take_action("not_equal", actual, expect)
    return ret

_actions = {"equal": lambda a,e: a == e,
            "not_equal": lambda a,e: not a == e}
def _take_action(action, actual, expect):
    if expect is None:
        raise NoExpectException()

    action = _actions[action]
    return action(actual, expect)
