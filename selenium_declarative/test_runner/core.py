#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from ..parser.core import Parser
from ..assertions.tdd import TDD
from ..scm_parser.core import Parser as SCMParser
from expect import NoExpectException, Expect

class TestRunner:
    def __testcase_adapter(self, msg, *exprs):
        expanded_exprs = ["try"] + exprs + [["catch", Exception, ["assert", msg, "not_raise", None, None]]]
        return [expanded_exprs]

    def __expect_adapter(self, id):
        return self.expect.get(id)

    def __assert_adapter(self, tdd):
        def ss(__parser__, __peek__, msg, action, actual=None, expect=None):
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
        return ss

    def __init__(self, driver, url, test_path, expect_path):
        self.driver = driver
        self.url = url
        self.test_path = test_path
        self.expect_path = expect_path
        self.expect_path
        self.tdd = TDD()
        self.expect = Expect(self.expect_path)
        self.parser = Parser(driver, {"assert": self.__assert_adapter(self.tdd),
                                      "expect": self.__expect_adapter,
                                      "testcase": self.__testcase_adapter})

    def get_setup(self, paths):
        for path in paths:
            if os.path.basename(path).startswith("setup.") and os.path.isfile(path):
                with open(path) as f:
                    content = f.read()
                    return eval(content)
        return []

    def get_teardown(self, paths):
        for path in paths:
            if os.path.basename(path).startswith("teardown.") and os.path.isfile(path):
                with open(path) as f:
                    return eval(f.read())
        return []

    def get_testcase(self, path):
        codes = []
        names = os.listdir(path)
        paths = map(lambda name: os.path.join(path, name), names)
        sd_paths = filter(lambda name: name.endswith(".sd"), paths)
        setup = self.get_setup(sd_paths)
        teardown = self.get_teardown(sd_paths)

        testcase_paths = filter(lambda path: os.path.basename(path).startswith("testcase"), sd_paths)
        for p in testcase_paths:
            with open(p) as f:
                code = eval(f.read())
                codes = codes + setup + code + teardown

        return codes

    def get_testcases(self, paths):
        code = []
        for d in paths:
            code = code + self.get_testcase(d)

        return code

    def run(self):
        SCMParser().parse(self.test_path)

        names = os.listdir(self.test_path)
        paths = map(lambda name: os.path.join(self.test_path, name), names)
        sd_paths = filter(lambda name: name.endswith(".sd"), paths)
        dirs = filter(lambda path: os.path.isdir(path), paths)

        setupclass = self.get_setup(sd_paths)
        testcases = self.get_testcases(dirs)
        teardownclass = self.get_teardown(sd_paths)

        code = setupclass + testcases + teardownclass

        self.driver.get(self.url)
        self.parser.parse(code)

        for result in self.tdd.results:
            if isinstance(result["detail"], NoExpectException):
                self.expect.save(result["message"], result["actual"])
        self.expect.close()
        self.driver.close()
