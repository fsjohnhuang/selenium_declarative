#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time, uuid
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
        ctx.assert_rets.append({"id": id, "result": None, "expect": actual(ctx)})

def op_print_assert_ret(ctx):
    assert_ret = ctx.assert_rets[-1]
    if assert_ret["result"] is None:
        print("\033[1;44m OK \033[0m {0}: collected expected value {1}.".format(assert_ret["id"], assert_ret["expect"]))
    elif assert_ret["result"]:
        print("\033[1;44m OK \033[0m {0}".format(assert_ret["id"]))
    else:
        print("\033[1;41m Fail \033[0m {0}: expect {1}, but acutal value is {2}".format(assert_ret["id"], assert_ret["expect"], assert_ret["actual"]))

def op_inject_ui_tips(ctx):
    ctx.slot["ui_dialog_id"] = str(uuid.uuid1()).split('-')[0]
    ctx.slot["ui_title_id"] = str(uuid.uuid1()).split('-')[0]
    ctx.slot["ui_content_id"] = str(uuid.uuid1()).split('-')[0]

    ctx.driver.execute_script("""
    var s_dialog = document.createElement('div');
    s_dialog.id = arguments[0];
    s_dialog.style.cssText = 'display:none;width:500px;box-shadow:1px 1px 10px 1px #bbb;border-radius:20px;position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);overflow:hidden;';

    var s_title = document.createElement('div');
    s_title.id = arguments[1];
    s_title.style.cssText = 'height:25px;background:#477EB8;font-size:18px;line-height:25px;padding:10px;color:#efefef;font-weight:bold;text-shadow:1px 1px 5px #bbb';
    s_title.textContent = 'Selenium Declarative Dialog';

    var s_content = document.createElement('div');
    s_content.id = arguments[2];
    s_content.style.cssText = 'height:200px;text-align:center;padding:20px;background:#fff;font-size:16px;font-weight:bold;';
    s_content.textContent = '测试';

    s_dialog.appendChild(s_title);
    s_dialog.appendChild(s_content);
    document.body.appendChild(s_dialog);
    """
    , ctx.slot["ui_dialog_id"]
    , ctx.slot["ui_title_id"]
    , ctx.slot["ui_content_id"])

def op_show_ui_tips(ctx, msg, sec):
    ctx.driver.execute_script("""
    var s_content = document.getElementById(arguments[2]);
    s_content.innerHTML = arguments[3];

    var s_dialog = document.getElementById(arguments[0]);
    s_dialog.style.display = 'block';
    setTimeout(function(){
        s_dialog.style.display = 'none';
    }, arguments[4]);
    """
    , ctx.slot["ui_dialog_id"]
    , ctx.slot["ui_title_id"]
    , ctx.slot["ui_content_id"]
    , msg
    , sec*1000)

    op_wait(ctx, sec)

def op_show_ui_assert_ret(ctx):
    assert_ret = ctx.assert_rets[-1]
    sec = 5
    if assert_ret["result"] is None:
        op_show_ui_tips(ctx, "<div>OK</div><div>{0}: collected expected value {1}.</div>".format(assert_ret["id"], assert_ret["expect"]), sec)
    elif assert_ret["result"]:
        op_show_ui_tips(ctx, "<font style='color:green;font-size:30px;font-weight:bold;'>✔</font><span>{0}</span>".format(assert_ret["id"]), 5)
    else:
        op_show_ui_tips(ctx, "<font style='color:red;font-size:30px;font-weight:bold;'>✘</font><span>{0}: expect {1}, but acutal value is {2}</span>".format(assert_ret["id"], assert_ret["expect"], assert_ret["actual"]), sec)

def op_show_ui_assert_summary(ctx):
    total = len(ctx.assert_rets)
    failure = 0
    success = 0
    for ret in ctx.assert_rets:
        if ret.get("result"):
            success += 1
        else:
            failure += 1
    op_show_ui_tips(ctx, "Tests ran {total}, <font style='color:green;font-weight:bold;'> Successes {success} </font>, <font style='color:red;font-weight:bold;'> Failures {failure} </font>".format(total=total, success=success, failure=failure), 10)
