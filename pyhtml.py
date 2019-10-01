#! /usr/bin/python
#
import sys


def LeftTag(tag_name, **kwargs):
   pattern = "<{}{}>"
   attrs = " ".join("{}{}{}".format(k,"=" if v else "",v) for k,v in kwargs.items())
   if attrs:
     attrs = " "+attrs
   return pattern.format(tag_name, attrs)


def Tag(tag_name, *args, **kwargs):
   pattern = "{}{}</{}>"
   text = "".join(args)
   return pattern.format(LeftTag(tag_name, **kwargs), text, tag_name)


def JavaScript(txt):
   #patern = "<script type=\"text/javascript\">\n%s\n</script>\n"
   #return patern % (txt,)
   dt={"type":"\"text/javascript\""}
   return Tag("script", txt, **dt)
  
def JavaScriptInc(txt):
   #patern = "<script type=\"text/javascript\" src=\"%s\"></script>\n"
   #return patern % (txt,)
   dt={"type":"\"text/javascript\""}
   return Tag("script", "", **dt)
  
def Label(txt, **kwargs):
   #patern = "<a>%s</a>\n"
   #return patern % (name, )
   return Tag("a", txt, **kwargs)

def Paragraph(txt):
   #patern = "<p>%s</p>\n"
   #return patern % (txt,)
   return Tag("p", txt)

def PH(txt):
   return Paragraph(txt)

def Header(txt, val=1):
   #patern = "<h1>%s</h1>\n"
   #return patern % (txt,)
   return Tag("h{}".format(val), txt)

def H1(txt):
   return Header(txt)

def H2(txt):
   return Header(txt, 2)

def H3(txt):
   return Header(txt, 3)

def H4(txt):
   return Header(txt, 4)


def Button(name, text="", onclc=""):
   if (text == ""): text = name
   if (onclc == ""): patern = "<button id=%s%s>%s</button>\n"
   else: patern = "<button id=%s onclick=\"%s;\">%s</button>\n"
   return patern % (name, onclc, text)

def TypeInput(tp,  **kwarg):
   dt = kwarg.copy()
   dt["type"] = tp;
   return LeftTag("input", **dt)

def SubmitButton(txt):
   #patern = "<input type=submit value=%s>\n"
   #return patern % (txt, )
   return TypeInput("submit", value=txt)

def CancelButton(txt):
   #patern = "<input type=reset value=%s>\n"
   #return patern % (name, )
   return TypeInput("reset", value=txt)

def Input(name, **kwargs):
   #strdis = ""
   #strval = ""
   #if disabled:
   #  strdis = " disabled"
   #if val:
   #  strval = " value="
   #patern = "<input name=%s%s%s%s>\n"
   #return patern % (name, strdis, strval, val)
   dt = kwargs.copy()
   dt["name"] = name
   return LeftTag("input", **dt)

def TextBox(name, val, disabled=False):
   return Label(name+":")+Input(name, value=val, disabled="")


def HyperLink(link, text=""):
   pref = "http://"
   if not text:
      text = link.replace(pref,"")

#   if link.lower().find(pref)==-1:
#      link = pref + link
 
   #patern = "<a href=\"%s\">%s</a>\n"
   #return patern % (link, text)
   return Label(text, href=link)


def InputCheckBox(name, **kwargs):
   #chtxt = ""
   #if ch : chtxt = "checked"
   #patern = "<input type=checkbox name=%s %s>\n"
   #return patern % (name, chtxt)
   dt = kwargs.copy()
   return TypeInput("checkbox", **dt)

def CheckBox(name, ch, **kwargs):
   dt = kwargs.copy()
   dt["checked"]=ch
   return InputCheckBox(name, **dt)+Label(name)

def NL():
   return "<br>\n"

def BR():
   return NL()

#<<tables   
def TableElement(eltype, tp):
   res = ""
   attr = ""
   ttp = TupleToString(tp)
   res = ttp[0]
   attr = ttp[1]

   eltype.lower()
   if eltype.startswith("td"):
      attr = attr.replace("cs=","colspan=")
   elif eltype.startswith("table"):
      attr = attr.replace("cs=","cellspacing=")
      attr = attr.replace("br=","border=")
      attr = attr.replace("wd=","width=")

   if (not attr.startswith(" ")) and (attr):
      attr = " "+attr
 
   patern = "<%s%s>%s</%s>\n"
   return patern % (eltype, attr, res, eltype)

def TableCell(*tp):
   return TableElement("td", tp)

def TableRow(*tp):
   return TableElement("tr", tp)

def TableLine(*tp):
   res = tuple(map(TD,tp)) + ("",)
   return TableElement("tr", res)

def TableHead(*tp):
   res = tuple(map(TH,tp)) + ("",)
   return TableElement("tr", res)

def Table(*tp):
   return TableElement("table", tp)

def TD(*tp):
   return TableElement("td", tp)

def TR(*tp):
   return TableElement("tr", tp)

def TH(*tp):
   return TableElement("th", tp)
#tables>>

def SQLTable(rows, name=""):
   res = ""
   alt = 2
   for row in rows:
      tmp = ""
      #header
      if alt == 2:
         for col in row:
            tmp = tmp + TH(str(col))
         res = res + TR(tmp)
         alt = 0
      #alt
      elif alt == 1:
         for col in row:
            tmp = tmp + TD(str(col))
         res = res + TR(tmp,{"class":"\"alt\""})
         alt = 0

      else:
         for col in row:
            tmp = tmp + TD(str(col))
         res = res + TR(tmp)
         alt = 1

   if name == "": res = Table(res,)      
   else: res = Table(res, "id="+name)
   return res


def DictToString(dt):
   res = ""
   if not dt:
      res = ""
   elif isinstance(dt, basestring):
      res = dt
   elif isinstance(dt, dict):
      for el in dt:
         res = res + "".join((" ", el, "=", str(dt[el])))

   return res

def TupleToString(tp):
   res = ""
   attr = ""
   if not tp:
      res = ""
   elif isinstance(tp, basestring):
      res = tp
   elif isinstance(tp, (list, tuple)):
      if len(tp)>1:
         res = "".join(tp[:-1])
         attr = DictToString(tp[-1])
      else:
         res = "".join(tp)

   return (res, attr)

def Form(name, *tp):
   ttp = TupleToString(tp)
   res = "<form name=%s method=post%s>\n %s </form>" % (name,ttp[1],ttp[0])
   return res

def Html(name, *tp):
   ttp = TupleToString(tp)
   res = "Content-Type: text/html\n\n"
   res = res + "<html>\n<head>\n<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\"/>\n"
   res = res + "<title>%s</title>\n<link rel=\"stylesheet\" type=\"text/css\" href=\"pyhtml-main.css\"/>\n"
   res = res + "</head><body>\n%s\n</body>\n</html>"
   #print res 
   res = res % (name, ttp[0])
   return res


#example
if __name__ == "__main__":

  print(Html("MyHtml module test",
    Form("myhtml.py", 
    Header("My Html"),
    Label("Students assessment:"), 
    Table(TableHead("N","Name","Surname",  "Mark"),        #TR(TH("N"),  TH("Name"),    TH("Surname"),   TH("Mark"),""),
      TableLine("1.", "John", "Doe",       Input("tst1")), #TR(TD("1."), TD("John"),    TD("Doe"),       TD(Input("tst1")),""),
      TR(TD("2."), TD("Michael"), TD("Cooperman",  "cs=2"),""),
      TableLine("3.", "Mark", "Lieberman", Input("tst3")), #TR(TD("3."), TD("Mark"),    TD("Lieberman"), TD(Input("tst3")),""),
      TableLine("4.", "Alex", "Miller",    Input("tst4")), #TR(TD("4."), TD("Alex"),    TD("Miller"),    TD(Input("tst4")),""),
    {"cs":1,"br":1} #"cs=1 br=1"
    ), 
    HyperLink("google.com"),
    NL(),
    NL(),
    CheckBox("manual", True),
    NL(),
    TextBox("test","111"),
    BR(),
    SubmitButton("save"),
    CancelButton("cancel"),
    Paragraph("%s %s" % (sys.version, sys.path)),
    "")))
