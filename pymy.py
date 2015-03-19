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


def SQLView(host,usr,pasw,db,query):
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
    rows.insert(0,tuple([i[0] for i in c.description]))

  except:
    conn.close()
    return mh.PH("Error command")

  conn.close()
  return SQLTable(rows)


#example
if __name__ == "__main__":

  print(mh.Html("MyHtml module test",
    mh.Form("myhtml.py", 
    mh.Header("My Html"),
    mh.Label("base:"), 
    SQLView("localhost","root","","main","SELECT * FROM termometrs;"),
    mh.SubmitButton("save"),
    mh.CancelButton("cancel"), 
    "")))
