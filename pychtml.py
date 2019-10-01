#! /usr/bin/python
#

class Tag(object):
  pref = ""
  mask = "{}<{}{}>{}</{}>"
  name = ""
  data = tuple()
  attrs = {}

  def __init__(self, name, *arg, **kwargs):
    self.name = name
    self.attrs = kwargs
    if arg:
      self.data = arg

  def __iter__(self):
    return self

  def render_attrs(self):
    tmp = ""
    if self.attrs:
      tmp = " "+" ".join(["{}='{}'".format(k, v) for k,v in self.attrs.items()])

    return tmp

  def render_data(self):
    tmp = ""
    for t in self.data:
      if isinstance(t, str):
        tmp = tmp + t
      else:
        tmp = tmp + t.render()
    return tmp

  def render(self, short=False):
    if short:
      return self.mask.format("", self.name, self.render_attrs(), "...", self.name)
    else:
      return self.mask.format(self.pref, self.name, self.render_attrs(), self.render_data(), self.name)

  def __str__(self):
    return self.render()


class SimTag(Tag):
  name = ""

  def __init__(self, *arg):
    super(SimTag, self).__init__(self.name, *arg)


class BigTag(Tag):
  name = ""

  def __init__(self, *arg, **kwarg):
    super(BigTag, self).__init__(self.name, *arg, **kwarg)


class Html(SimTag):
  pref = "<!DOCTYPE html>"
  name = "html"

class Body(SimTag):
  name = "body"

class Head(SimTag):
  name = "head"

class Table(BigTag):
  name = "table"

class TBody(BigTag):
  name = "tbody"

class TH(BigTag):
  name = "th"

class TR(BigTag):
  name = "th"

class TD(BigTag):
  name = "td"

class P(BigTag):
  name = "p"

class A(BigTag):
  name = "a"

  def render_data(self):
    if len(self.data)==0:
      if "href" in self.attrs:
        self.data = self.data + (self.attrs["href"],)
    return super(BigTag, self).render_data()

class Div(BigTag):
  name = "div"

class Title(SimTag):
  name = "title"

class H1(SimTag):
  name = "h1"


if __name__ == "__main__":
  
  print "Content-Type: text/html\n\n"
  print Html(Title("test"), 
          Head(), 
          Body( H1("test of test"), 
              P("Lorem impsum web hren"), 
              A(href="test.html"), 
              Table( TR( TD(), TD() ), id="test")
          )
        )