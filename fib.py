#!/usr/bin/env python

import wsgiref.handlers
from google.appengine.ext import webapp

class MainPage(webapp.RequestHandler):
	def get(self):
		self.response.out.write("""
			<html><body>
			<h1>Fibonacci printer</h2>
			How long should the counter print numbers?<br/>
			<form action="/fib" method="post">
        		<div><input name="content" </input></div>
        		<div><input type="submit" value="Calculate"></div>
       		 	</form>
    			</body>
      			</html>
		""")

class RunFib(webapp.RequestHandler):
	#Method 1, recursive
	def fib(self, a, b, i, j):
		if j>i:
			return
		c = a + b
		self.response.out.write(str(c)+", ")
		self.fib(b, c, i, j+1)

	#Method 2, recursive (to recursive):
	def fib2(self, n):
		if n == 0: 
			return 0
		elif n == 1: 
			return 1
		else: 
			a = self.fib2(n-1)+self.fib2(n-2)
			return a

	#Method 3, iterative
	def fibi(self, n):
		a = 0
		b = 1
		for i in xrange(n):
			c = a+b
			a = b
			b = c
			self.response.out.write(str(c)+", ")

	#post method, will be called when MainPage does a post
	def post(self):
		self.response.out.write('<html><body>')
		antall = self.request.get('content')
		self.response.out.write("Calculating the fibonacci-sequence for "+antall+" numbers: <br/><br/>")
		self.fibi(int(antall))	
		self.response.out.write('</body></html>')

application = webapp.WSGIApplication([
  ('/', MainPage),
  ('/fib', RunFib)
], debug=True)


def main():
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
