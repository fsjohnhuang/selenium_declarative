#!/usr/bin/env python
# -*- coding: utf-8 -*-
from functools import partial
from parser import Parser
from assertions.tdd import TDD
from expect import NoExpectException, Expect

def __testcase_adapter(msg, *exprs):
    expanded_exprs = ["try"] + [expr for expr in exprs] + [["catch", Exception, ["assert", msg, "not_raise", None, None]]]
    return [expanded_exprs]

def __expect_adapter(id):
    return expect.get(id)

def __assert_adapter(tdd, __parser__, __peek__, msg, action, actual=None, expect=None):
    try:
        if actual is None:
            actual = __peek__()
        else:
            actual = __parser__.parse_with_sub_context(actual)
    except Exception, e:
        actual = e

    if isinstance(expect, list):
        expect.append(msg)
    try:
        expect = __parser__.parse_with_sub_context(expect)
    except Exception, e:
        expect = e

    ret = tdd.execute(action, actual, expect, msg)
    print(ret)

class TestRunner:

    def __init__(self, driver, url, test_path, expect_path):
        self.driver = driver
        self.url = url
        self.test_path
        self.expect_path
        self.tdd = TDD()
        self.expect = Expect(self.expect_path)
        self.parser = Parser(driver, {"assert": TestRunner.assert_adapter,
                                      "expect": TestRunner.expect_adapter,
                                      "testcase": TestRunner.testcase_adapter})
