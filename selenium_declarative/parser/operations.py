#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from inspect import isfunction
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

def op_switch_default_content(ctx):
    ctx.driver.switch_to.default_content()


_ops = {"eq": lambda a,e: a == e,
        "gt": lambda a,e: a > e,
        "gte": lambda a,e: a >= e}

def _do_assert(operator, actual, expect):
    if isfunction(operator):
        return operator(actual, expect)
    else:
        return _ops.get(operator)(actual, expect)

def _collect_expect(ctx, id, expect):
    ctx.collect_expects[id] = expect

def op_assert(ctx, id, operator, actual, expect = None):
    assert_ret = None
    if expect is None and id in ctx.expects:
        expect = ctx.expects.get(id)

    if not expect is None:
        actual = actual(ctx)
        assert_ret = _do_assert(operator, actual, expect)
        if assert_ret:
            ctx.assert_rets.append({"id": id, "result": True})
        else:
            ctx.assert_rets.append({"id": id, "result": False, "actual": actual, "expect": expect})
    else:
        _collect_expect(ctx, id, actual(ctx))
