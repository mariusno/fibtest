#!/usr/bin/env python

import wsgiref.handlers
from google.appengine.ext import webapp
from threading import Thread

class MainPage(webapp.RequestHandler):
	def get(self):
		self.response.out.write("""<html><body>""")
		self.response.out.write("""
			<h1>Fibonacci printer (iterative)</h2>
			How long should the counter print numbers?<br/>
			<form action="/fib" method="post">
        		<div><input name="content" </input></div>
        		<div><input type="submit" value="Calculate"></div>
       		 	</form>""")

		self.response.out.write("""
			<h1>Fibonacci printer2 (threaded)</h2>
			Which number do you want?<br/>
			<form action="/fib2" method="post">
        		<div><input name="content" </input></div>
        		<div><input type="submit" value="Calculate"></div>
       		 	</form>""")



		self.response.out.write("""</body></html>""")

class RunFibT(webapp.RequestHandler):
	def fibt(self,n,r):
		if n == 0: r[0]= 0
		elif n == 1: r[0] = 1
		else:
			res1 = [None]
			res2 = [None]
			t = Thread(target=self.fibt, args=(n-1,res1))
    			t.start()
			y = Thread(target=self.fibt, args=(n-2,res2))
    			y.start()
			#Join the threads, so they will terminate at the same time
			y.join()
			t.join()
			r[0] = res1[0]+res2[0]


	def post(self):
		self.response.out.write('<html><body>')
		antall = self.request.get('content')
		self.response.out.write("Calculating the "+antall+" fibonacci number: <br/><br/>")
		
		res = [None]
		self.fibt(int(antall),res)
		self.response.out.write(res[0])
		self.response.out.write('</body></html>')



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

	#Method 3, iterative (this metod returns one to many, because it only prints the first "1")
	def fibi(self, n):
		a = 1
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
  ('/fib', RunFib),
  ('/fib2', RunFibT)
], debug=True)


def main():
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
