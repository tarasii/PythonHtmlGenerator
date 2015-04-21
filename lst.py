#! /usr/bin/python
#
import pyhtml as mh
import mysql.connector
import cgi
import os
import myvrs

def qdNorm(qd=""):
  res = {'tbl':'','srt':'','dsc':'','id':'','lnk':'','lim':0}
  if isinstance(qd, basestring):
    res['table'] = qd
  elif isinstance(qd, dict):
    for key in res:
      if key in qd: res[key]=qd[key]
  
  res['lnk'] = __file__.replace('./','')

  if 'REQUEST_METHOD' in os.environ :
    form = cgi.FieldStorage()
    res['lnk'] = os.environ['SCRIPT_NAME']
    for key in res:
      if key in form: res[key]=form.getvalue(key)

  return res
 
def srhl(qd, val):
  if qd['tbl']=="": res = val
  else:
    if (qd['srt']==val)and(qd['dsc']==""): 
    #if (qd['srt']==val): 
      res = mh.HyperLink(qd['lnk']+"?tbl="+qd['tbl']+"&dsc=1&srt="+val, val)
    else:
      res = mh.HyperLink(qd['lnk']+"?tbl="+qd['tbl']+"&srt="+val, val)
  return res

def srhlq(qd, val):
  res = qd['lnk']+"?"
  #if qd['srt']<>"":
    #res = res +"&srt="+qd['srt']
  #if qd['dsc']<>"":
    #res = res +"&dsc="+str(qd['dsc'])
  
  if (qd['srt']==val)and(qd['dsc']==""): 
    res = res + "&dsc=1&srt=" + val
  else:
    res = res + "&srt=" + val

  if qd['lim']<>"":
    res = res +"&lim="+str(qd['lim'])
  
  return mh.HyperLink(res, val)

def idhl(qd, val):
  if qd['tbl']=="":
    res = mh.HyperLink(qd['lnk']+"?tbl="+str(val),str(val))
  else:
    res = mh.HyperLink(qd['lnk']+"?tbl="+qd['tbl']+"&id="+str(val),str(val))
  return res

def nxthl(qd, val):
  res = qd['lnk']+"?"
  if qd['tbl']<>"":
    res = res +"&tbl="+qd['tbl']
  if qd['id']<>"":
    res = res +"&id="+str(qd['id'])
  if qd['srt']<>"":
    res = res +"&srt="+qd['srt']
  if qd['dsc']<>"":
    res = res +"&dsc="+str(qd['dsc'])
  if qd['lim']<>"":
    res = res +"&lim="+str(qd['lim'])
  return mh.HyperLink(res, val)

def TabelLister(host,usr,pasw,db,name,qparam=""):
  res = mh.Paragraph("null");
  try:
    conn = mysql.connector.connect(
      host=host, user=usr, passwd=pasw, database=db)
  
  except:
    return mh.PH("Error connection")

  c = conn.cursor()
  #rowscnt = 0;

  qd = qdNorm(qparam)

  if (qd['tbl'] == ""): 
    query = "SHOW TABLES"
    querylim = query 
    descr = "tables list:"
    back = ""
  else:
    query = "SELECT * FROM " + qd['tbl']
    descr = qd['tbl']
    if (qd['id'] <> ""): 
      query = query + " WHERE id = " + qd['id']
      #descr = descr + " id = " + curid

    if (qd['srt'] <> ""): 
      query = query + " ORDER BY " + qd['srt']
      descr = descr + " by " + qd['srt']

    if (qd['dsc'] <> ""): 
      query = query + " DESC "
      descr = descr + "-" 
    else:
      descr = descr + "+" 
    
    #if (rowscnt > 25): 
    querylim = query + " LIMIT "+str(int(qd['lim'])*25)+", 25"
    descr = descr + ":"
    back = mh.HyperLink("pytable.py","all tables") 

  try:
    #c.execute("SELECT COUNT(*) from ("+query+") as cnttbl")
    #rowscnt = c.fetchone()[0]
    
    c.execute(querylim)
    rows = c.fetchall()

  except:
    conn.close()
    return mh.PH("Error command: "+querylim)

  #conn.close()

  #rows.insert(0,tuple([i[0] for i in c.description]))
  #newrows = [tuple([i[0] for i in c.description])]

  newrows = [tuple([srhl(qd,i[0]) for i in c.description])]

  for row in rows:
    #newrows.append(row)
    if len(row)==0:
      newrows.append(row)
    elif len(row)==1 and qd['tbl'] == "":
      newrows.append((idhl(qd,row[0]),))
    elif len(row)==1:
      newrows.append(row)
    else:
      newrows.append((idhl(qd,row[0]),)+row[1:])
  
    #newrows.append((rowscnt,))
  
  if (qd['tbl'] <> ""): 
    tmplim = int(qd['lim'])
    if tmplim >0:
      qd['lim'] = str(tmplim - 1) 
      back = back + nxthl(qd,'prev')

    querylim = query + " LIMIT "+str((tmplim+1)*25)+", 1"

    try:
      c.execute(querylim)
      rows = c.fetchall()
      if len(rows)>0:
        qd['lim'] = str(tmplim + 1) 
        back = back + nxthl(qd,'next')

    except:
      conn.close()
      #return mh.PH("Error command")
  

  conn.close()

  back = back + mh.BR()

  #return mh.SQLTable(newrows,"tbl1")+mh.Label("total rows:"+str(rowscnt))+mh.BR()
  return back + mh.Label(descr) + mh.SQLTable(newrows, name)

def QueryLister(host,usr,pasw,db,name,query):
  res = mh.Paragraph("null");
  try:
    conn = mysql.connector.connect(
      host=host, user=usr, passwd=pasw, database=db)
  
  except:
    return mh.PH("Error connection")

  c = conn.cursor()

  qd = qdNorm("")

  descr = "query "+name
  if (qd['srt'] <> ""): 
    query = query + " ORDER BY " + qd['srt']
    descr = descr + " by " + qd['srt']

  if (qd['dsc'] <> ""): 
    query = query + " DESC "
    descr = descr + "-" 
  else:
    descr = descr + "+" 
    
  querylim = query + " LIMIT "+str(int(qd['lim'])*25)+", 25"
  descr = descr + ":"

  try:
    c.execute(querylim)
    rows = c.fetchall()

  except:
    conn.close()
    return mh.PH("Error command: "+querylim)

  #conn.close()

  #newrows = [tuple([i[0] for i in c.description])]
  newrows = [tuple([srhlq(qd,i[0]) for i in c.description])]
  for row in rows:
    newrows.append(row)

  #rows.insert(0,tuple([i[0] for i in c.description]))
  
  back = ""
  tmplim = int(qd['lim'])
  if tmplim >0:
    qd['lim'] = str(tmplim - 1) 
    back = back + nxthl(qd,'prev')

  querylim = query + " LIMIT "+str((tmplim+1)*25)+", 1"

  try:
    c.execute(querylim)
    rows = c.fetchall()
    if len(rows)>0:
      qd['lim'] = str(tmplim + 1) 
      back = back + nxthl(qd,'next')

  except:
    conn.close()

  conn.close()

  back = back + mh.BR()

  return back + mh.Label(descr) + mh.SQLTable(newrows, name)


#example
if __name__ == "__main__":
  print TabelLister(myvrs.srv, myvrs.usr, myvrs.pwd, myvrs.base, "tbl1")  

