#! /usr/bin/python
#
import pyhtml as mh
import lst
import myvrs

import cgitb
cgitb.enable()

#example
if __name__ == "__main__":

  print(mh.Html("MyHtml mysql tabel list",
    mh.JavaScriptInc("js/jquery-1.8.2.js"),
    mh.JavaScript("console.log('start');"),
    mh.Header("Main:"),
    lst.TabelLister(myvrs.srv, myvrs.usr,  myvrs.pwd, myvrs.base, "tbl1"),
    ""))
