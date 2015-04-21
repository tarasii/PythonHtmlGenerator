#! /usr/bin/python
#
import pyhtml as mh
import mysql.connector
import myvrs

def QueryLister(host,usr,pasw,db,query):
  res = mh.Paragraph("null");
  try:
    conn = mysql.connector.connect(
      host=host, user=usr, passwd=pasw, database=db)
  
  except:
    return mh.PH("Error connection")

  c = conn.cursor()

  try:
    c.execute(query)
    rows = c.fetchall()
      #row[0] = mh.HyperLink(row[0])
      #row[0] =  mh.HyperLink(row[0])

    newrows = [tuple([i[0] for i in c.description])]
    for row in rows:
      #newrows.append([mh.HyperLink("pytable.py?table="+row[0],row[0]),])
      #row = ([mh.HyperLink("pytable.py?table="+row[0],row[0]),])
      newrows.append(row)

    #rows.insert(0,tuple([i[0] for i in c.description]))

  except:
    conn.close()
    return mh.PH("Error command")

  conn.close()

  return mh.SQLTable(newrows,"tbl1")


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
    QueryLister(myvrs.srv, myvrs.usr,  myvrs.pwd, myvrs.base, "SELECT * FROM temperatures ORDER BY id DESC LIMIT 0, 25 "),
    #mh.Button("clr","clear",strfn), 
    #mh.Button("nrm","norm","$('#tbl1').show()"), 
    #mh.HyperLink("javascript:alert('You clicked!')","test"), 
    ""))
