#! /usr/bin/python
#
import pyhtml as mh
import mysql.connector


def SQLTable(rows):
   res = ""
   alt = 2
   for row in rows:
      tmp = ""

      if alt==2:
         for col in row:
            tmp = tmp + mh.TH(str(col))
         res = res + mh.TR(tmp)
         alt = 0

      elif alt==1:
         for col in row:
            tmp = tmp + mh.TD(str(col))
         res = res + mh.TR(tmp,{"class":"\"alt\""})
         alt = 0

      else:
         for col in row:
            tmp = tmp + mh.TD(str(col))
         res = res + mh.TR(tmp)
         alt = 1
      
   res = mh.Table(res)
   return res

def trySQL():
  res = "";
  try:
    conn = mysql.connector.connect(host="localhost", 
                     user="root", 
                      passwd="aceofbase", database='main')  
  except:
    #print ("Error connection")
    return ("Error connection",)

  c = conn.cursor()

  try:
    #c.execute('SHOW TABLES;')
    c.execute('SELECT * FROM termometrs;')
    rows = c.fetchall()
    rows.insert(0,tuple([i[0] for i in c.description]))
    #print rows
    #res = SQLTable(rows)

  except:
    #print ("Error command")
    conn.close()
    return ("Error command",)

  conn.close()
  return rows


#example
if __name__ == "__main__":
  rws = trySQL()
  #print str(rws)

  print(mh.Html("MyHtml module test",
    mh.Form("myhtml.py", 
    mh.Header("My Html"),
    mh.Label("base:"),
    #mh.Paragraph(rws), 
    SQLTable(rws),
    mh.SubmitButton("save"),
    mh.CancelButton("cancel"), 
    "")))
