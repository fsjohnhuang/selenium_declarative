#!/usr/bin/env python
# -*- coding: utf-8 -*-

def expr_find_element(ctx, slctr_type, slctr, *ops):
    el = None
    try:
        el = ctx.driver.find_element(slctr_type, slctr)
    except Exception, e:
        el = None
    ctx.expr_rets.append(el)
    ctx.parse(ops)

def expr_find_elements(ctx, slctr_type, slctr, *ops):
    els = None
    try:
        els = ctx.driver.find_elements(slctr_type, slctr)
    except Exception, e:
        els = None
    ctx.expr_rets.append(els)
    ctx.parse(ops)

def expr_clickable(ctx):
    el = ctx.expr_rets[-1]
    ctx.expr_rets.append(not el is None and el.is_displayed())

def expr_unclickable(ctx):
    el = ctx.expr_rets[-1]
    ctx.expr_rets.append(el is None or not el.is_displayed())
