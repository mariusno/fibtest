#!/usr/bin/env python

import cgi
import datetime
import wsgiref.handlers

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp

class Greeting(db.Model):
  author = db.UserProperty()
  content = db.StringProperty(multiline=True)
  date = db.DateTimeProperty(auto_now_add=True)


class MainPage(webapp.RequestHandler):
  def get(self):
    self.response.out.write('<html><body>')

    self.response.out.write("""
          <form action="/fib" method="post">
            <div><input name="content" </input></div>
            <div><input type="submit" value="Calculate"></div>
          </form>
        </body>
      </html>""")

class RunFib(webapp.RequestHandler):
	#Method 1:
	def fib(self, a, b, i, j):
		if j>i:
			return
		c = a + b
		self.response.out.write(str(c)+" ")
		self.fib(b, c, i, j+1)

	#Method 2, (to recursive):
	def fib2(self, n):
		if n == 0: return 0
		elif n == 1: return 1
		else: 
			a = self.fib2(n-1)+self.fib2(n-2)
			return a

	def post(self):
		greeting = Greeting()
		self.response.out.write('<html><body>')
		antall = self.request.get('content')
		self.response.out.write("Regner ut for "+antall+" antall fib-tall <br/>")
		self.fib(1,1,int(antall),1)	
		#self.response.out.write("prover andre</br>")
		#a = self.fib2(int(antall))	
		#self.response.out.write(a)
		self.response.out.write('</html></body>')

application = webapp.WSGIApplication([
  ('/', MainPage),
  ('/fib', RunFib)
], debug=True)


def main():
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
