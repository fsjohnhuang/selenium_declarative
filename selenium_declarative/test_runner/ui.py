#!/usr/bin/env python
# -*- coding: utf-8 -*-

_dialog_tpl = """
var s_dialog = document.createElement('div');
s_dialog.id = arguments[0];
s_dialog.style.cssText = 'font-family:"Microsoft YaHei", SimHei, SimSun;display:none;width:500px;box-shadow:2px 2px 20px 5px #777;border-radius:10px;position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);overflow:hidden;';

var s_title = document.createElement('div');
s_title.id = arguments[1];
s_title.style.cssText = 'height:25px;background:#477EB8;font-size:18px;line-height:25px;padding:10px;color:#ffffef;font-weight:bold;text-shadow:1px 1px 0px #ababab;';
s_title.textContent = 'Selenium Declarative Dialog';

var s_content = document.createElement('div');
s_content.id = arguments[2];
s_content.style.cssText = 'text-align:center;padding:20px;background:#fff;color:#333;font-size:16px;font-weight:bold;';

s_dialog.appendChild(s_title);
s_dialog.appendChild(s_content);
document.body.appendChild(s_dialog);
"""
def inject_dialog(ctx):
    id = str(uuid.uuid1()).split('-')[0]
    ctx.slot["ui_dialog_id"] = "sd-dialog-" + id
    ctx.slot["ui_title_id"] = "sd-title-" + id
    ctx.slot["ui_content_id"] = "sd-content-" + id

    ctx.driver.execute_script(
        _dialog_tpl
        , ctx.slot["ui_dialog_id"]
        , ctx.slot["ui_title_id"]
        , ctx.slot["ui_content_id"])


_show_dialog_script = """
var s_content = document.getElementById(arguments[2]);
s_content.innerHTML = arguments[3];

var s_dialog = document.getElementById(arguments[0]);
s_dialog.style.display = 'block';
setTimeout(function(){
    s_dialog.style.display = 'none';
}, arguments[4]);
"""
def show_dialog(ctx, msg, sec=2):
    ctx.driver.execute_script(
        _show_dialog_script
        , ctx.slot["ui_dialog_id"]
        , ctx.slot["ui_title_id"]
        , ctx.slot["ui_content_id"]
        , msg
        , sec*1000)

_starting_dialog_tpl = """
<p style='font-size:30px;padding:5px;color:#343434;text-shadow:1px 1px #898989;'>UI Automation Test <br> Starts <span id="{0}" style="color:red;">{1}</span>s Later!</p>
"""
_staring_dialog_script = """
var t = document.getElementById(arguments[0]);
var si = setInterval((function(i){
    return function(){
        t.textContent = --i;
        if (i <= 0){
            clearInterval(si)
        }
    }
}(arguments[1])), 1000);
"""
def show_starting_dialog(ctx, sec=3):
    sec_id = str(uuid.uuid1()).split("-")[0]
    show_dialog(ctx, _starting_dialog_tpl.format(sec_id, sec), sec)
    ctx.driver.execute_script(
        _staring_dialog_script
        , sec_id
        , sec)


_assert_ret_tpl1 = """
<div style='text-align:left;color:#454545;margin-bottom:15px;font-size:24px;'>Assertion: {0}</div>
<div style="float:left;height:50px;width:50px;padding:20px;line-height:50px;font-size:60px;margin-right:20px;color:#fff;background:{2};border-radius:50%;">{1}</div>
<div style="float:left;color:#666;text-align:left;">
    <p><b>Expect:</b> {3}</p>
    <p><b>Actual:</b> {4}</p>
</div>
<div style='clear:both'></div>
"""
_assert_ret_tpl2 = """
<div style='text-align:left;color:#454545;margin-bottom:15px;font-size:24px;'>Assertion: {0}</div>
<div style="float:left;height:50px;width:50px;padding:20px;line-height:50px;font-size:60px;margin-right:20px;color:#fff;background:orange;border-radius:50%;">!</div>
<div style="float:left;color:#666;text-align:left;">
    <p><b>Discovered a new guy as expect:</b></p>
    <p>{1}</p>
</div>
<div style='clear:both'></div>
"""
def show_assert_ret(ctx, sec=2):
    assert_ret = ctx.assert_rets[-1]
    if assert_ret["result"] is None:
        op_show_ui_tips(ctx, _assert_ret_tpl2.format(assert_ret["id"], assert_ret["expect"]), sec)
    elif assert_ret["result"] == Exception:
        op_show_ui_tips(ctx, _assert_ret_tpl1.format(assert_ret["id"], "！", "yellow", assert_ret["expect"], ""), sec)
    elif assert_ret["result"]:
        op_show_ui_tips(ctx, _assert_ret_tpl1.format(assert_ret["id"], "✔", "green", assert_ret["expect"], assert_ret["actual"]), sec)
    else:
        op_show_ui_tips(ctx, _assert_ret_tpl1.format(assert_ret["id"], "✘", "red", assert_ret["expect"], assert_ret["actual"]), sec)


_assert_summary_tpl = """
<div style='text-align:left;color:#454545;margin-bottom:15px;font-size:24px;'>Summary</div>
<div style='text-align:left;color:#666;margin-bottom:10px;font-size:20px;padding-left:20px;'><b>Total:</b>{0}</div>
<div style='text-align:left;color:green;margin-bottom:10px;font-size:20px;padding-left:20px;'><b>Success:</b>{1}</div>
<div style='text-align:left;color:red;margin-bottom:10px;font-size:20px;padding-left:20px;'><b>Failure:</b>{2}</div>
<div style='text-align:left;color:orange;margin-bottom:10px;font-size:20px;padding-left:20px;'><b>Other:</b>{3}</div>
"""
def show_assert_summary(ctx, sec=5):
    total = len(ctx.assert_rets)
    failure = 0
    success = 0
    other = 0
    error = 0
    for ret in ctx.assert_rets:
        result = ret.get("result")
        if result is None:
            other += 1
        elif result == Exception:
            error += 1
        elif result:
            success += 1
        else:
            failure += 1
    op_show_ui_tips(ctx, _assert_summary_tpl.format(total, success, failure, other), sec)
