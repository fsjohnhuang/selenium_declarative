#!/usr/bin/env python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium_declarative.test_runner.core import TestRunner

def main():
    driver = webdriver.Chrome()
    t = TestRunner(driver, "http://gqms.midea.com", "/home/john/selenium_declarative/test", "/home/john/sd.test")

    t.run()
main()
