#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from selenium.webdriver.common.action_chains import ActionChains

def expr_find_element(__driver__, slctr_type, slctr):
    return __driver__.find_element(slctr_type, slctr)

def expr_find_element_safe(__driver__, slctr_type, slctr):
    try:
        return __driver__.find_element(slctr_type, slctr)
    except Exception, e:
        return e

def expr_find_elements(__driver__, slctr_type, slctr):
    return __driver__.find_elements(slctr_type, slctr)

def expr_find_elements_safe(__driver__, slctr_type, slctr):
    try:
        return __driver__.find_elements(slctr_type, slctr)
    except Exception, e:
        return e

def expr_click(__peek__, slctr_type=None, slctr=None):
    if slctr_type is not None and slctr is not None:
        return [["find_element", slctr_type, slctr], ["click"]]
    else:
        el = __peek__()
        el.click()

def expr_dblclick(__driver__, __peek__, slctr_type=None, slctr=None):
    if slctr_type is not None and slctr is not None:
        return [["find_element", slctr_type, slctr], ["dblclick"]]
    else:
        el = __peek__()
        ActionChains(__driver__).double_click(el).perform()

def expr_send_keys(__peek__, key):
    el = __peek__()
    el.send_keys(key)

def expr_wait(sec):
    time.sleep(sec)

def expr_clickable(__peek__, slctr_type=None, slctr=None):
    if slctr_type is not None and slctr is not None:
        return [["find_element", slctr_type, slctr], ["clickable"]]
    else:
        el = __peek__()
        try:
            a = el.is_displayed()
            return a
        except Exception, e:
            raise False

def expr_switch_frame(__driver__, index=-1):
    count_frame = len(__driver__.find_elements("tag name", "iframe"))
    if index < 0:
        index = count_frame + index
    index = index % count_frame
    __driver__.switch_to.frame(index)

def expr_switch_default_content(__driver__):
    __driver__.switch_to.default_content()

def expr_count(__peek__):
    els = __peek__()
    return len(els)

def expr_display(__peek__, anything=None):
    """write anything to stdout in human-readable format."""
    anything = anything if anything is not None else __peek__()
    print(anything)
