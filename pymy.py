#! /usr/bin/python
#
import pyhtml as mh
import lst
import myvrs

#example
if __name__ == "__main__":
  strfn = """//console.log('test');
    //zz = document.getElementById('tbl1');
    //zz.remove();
    //zz.style.display = 'none';
    $('#tbl1').hide();
  """
  print(mh.Html("Mysql python table lister",
    mh.JavaScriptInc("js/jquery-1.8.2.js"),
    mh.JavaScript("console.log('start');"),
    mh.Header("Tables list:"),
    #QueryLister(myvrs.srv, myvrs.usr,  myvrs.pwd, myvrs.base, "SHOW TABLES;"),
    lst.QueryLister(myvrs.srv, myvrs.usr,  myvrs.pwd, myvrs.base, "view", "SELECT * FROM temperatures "),
    #mh.Button("clr","clear",strfn), 
    #mh.Button("nrm","norm","$('#tbl1').show()"),
    mh.BR(), 
    mh.Button("refresh","refresh","location.reload()"), 
    #mh.HyperLink("javascript:alert('You clicked!')","test"), 
    ""))
