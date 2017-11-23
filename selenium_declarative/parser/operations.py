#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from selenium.webdriver.common.action_chains import ActionChains

def op_click(ctx):
    """
    Usage:
    [click]
    """
    el = ctx.expr_rets[-1]
    el.click()

def op_dblclick(ctx):
    """
    Usage:
    [dblclick]
    """
    el = ctx.expr_rets[-1]
    ActionChains(ctx.driver).double_click(el).perform()

def op_send_keys(ctx, val):
    """
    Usage:
    [send_keys val]
    """
    el = ctx.expr_rets[-1]
    el.send_keys(val)

def op_wait(ctx, sec):
    time.sleep(sec)

def op_switch_frame(ctx, idx = -1):
    count_frame = len(ctx.driver.find_elements("tag name", "iframe"))
    if idx < 0:
        idx = count_frame + idx
    idx = idx % count_frame
    ctx.driver.switch_to.frame(idx)
