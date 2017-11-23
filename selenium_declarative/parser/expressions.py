#!/usr/bin/env python
# -*- coding: utf-8 -*-

def expr_find_element(ctx, slctr_type, slctr, *ops):
    el = ctx.driver.find_element(slctr_type, slctr)
    ctx.expr_rets.append(el)
    ctx.parse(ops)

def expr_find_elements(ctx, slctr_type, slctr, *ops):
    el = ctx.driver.find_elements(slctr_type, slctr)
    ctx.expr_rets.append(el)
    ctx.parse(ops)
