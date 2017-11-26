#!/usr/bin/env python
# -*- coding: utf-8 -*-
from inspect import isfunction
from test_runner.expect import NoExpectException

class TDD:
    __actions = {"equal": lambda a,e: a == e,
                 "not_equal": lambda a,e: not a == e}

    def __init__(self):
        self.__results = []

    @property
    def results(self):
        return self.__results

    def execute(self, action, actual, expect, message = ""):
        ret = {"result": 1, "detail": None, "message": message, "actual": actual, "expect": expect, "action": action}
        try:
            r = self.__do_execute(action, actual, expect)
            ret["result"] = 0 if r[0] else 1
            ret["expect"] = r[1]
        except Exception, e:
            ret["result"] = -1
            ret["detail"] = e
        self.__results.append(ret)

        return ret

    def __do_execute(self, action, actual, expect):
        ret = False
        if isfunction(actual):
            actual = actual()

        if "ok" == action:
            action = "equal"
            expect = True
        elif "not_ok" == action:
            action = "equal"
            expect = False

        ret = self.__take_action(action, actual, expect)
        return [ret, expect]

    def __take_action(self, action, actual, expect):
        if expect is None:
            raise NoExpectException()

        action = self.__actions[action]
        return action(actual, expect)
