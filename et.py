#!/usr/bin/env python
#
# This Works is placed under the terms of the Copyright Less License,
# see file COPYRIGHT.CLL.  USE AT OWN RISK, ABSOLUTELY NO WARRANTY. 

from __future__ import print_function
import sys
import re
from cStringIO import StringIO

class EtNoMatch(Exception):
	def __init__(self, state, msg):
		self.state = state
		self.msg = msg

	def __str__(self):
		return self.msg + ' in line '+str(self.state.n)+' column '+str(self.state.c)

class EtEl(object):
	def match(self, state):
		pass

	def eof(self, state):
		raise EtNoMatch(state, 'Unexpected EOF at '+str(self))

class EtElEOF(EtEl):
	def match(self, state):
		raise EtNoMatch(state, '['+state.l+'] Not at EOF')

	def eof(self, state):
		pass

class EtElEOL(EtEl):
	def match(self, state):
		if len(state.l):
			raise EtNoMatch(state, 'EOL, not matched: ['+state.l+']')
		state.p += 1

class EtElStr(EtEl):
	def __init__(self, s):
		self.s = s

	def match(self, state):
		if not state.l.startswith(self.s):
			raise EtNoMatch(state, '\nhave ['+state.l[0:len(self.s)]+']\nwant ['+self.s+']')
		state.ok(len(self.s))

	def __repr__(self):
		return 'EtElStr["'+self.s+'"]';

class EtElReg(EtEl):
	def __init__(self, r):
		self.r	= re.compile(r)
		self._r	= r

	def match(self, state):
		m = self.r.match(state.l)
		if not m:
			raise EtNoMatch(state, '['+state.l+'] does not match /'+self._r+'/')
#		state.m.append(m.group(0))
		state.m.extend(m.groups())
		state.ok(m.end())

class EtElFN(EtEl):
	def __init__(self, r):
		self.r	= re.compile(r)

	def match(self, state, l):
		raise Exception('not yet implemented')

class EtState(object):

	def __init__(self, t):
		self.t	= t
		self.m	= []
		self.p	= 0
		self.n	= 0
		self.c	= 0

	def ok(self, n):
		self.c	+= n
		self.l	=  self.l[n:]

	def step(self, l):
		self.n	+= 1
		self.c	= 1
		self.l = l[-1]!='\n' and l or l[:-1]
#debug		print(self.l)
		p = self.t[self.p]
		for a in self.t[self.p]:
			a.match(self)

	def eof(self):
		p = self.t[self.p]
		p[0].eof(self)

class EtCompile(object):
	"""internal class, can change without notice"""
	def __init__(self, template=None):
		self.compile(template)

	def string(self, e, t, s):
		s = [ s ]
		while e:
			if e[0]=='' and len(e)>1 and e[1].startswith('}'):
				e.pop(0)
				s.append('{')
				# falltrough
			if e[0].startswith('}'):
				s.append(e.pop(0)[1:])
			elif e[0].startswith('//}'):
				s.append(e.pop(0)[4:])
			else:
				break
		s = ''.join(s)
		if s:
			t.append(EtElStr(s))

	def compile(self, template):
		m	= []
		lines	 = template.split('\n')
		if lines and lines[-1]=='':
			lines.pop()
		for l in lines:
			t = []
			e = l.split('{')
			s = e.pop(0)
			self.string(e, t, s)
			while e:
				self.parse(e, t)
			t.append(EtElEOL())
			m.append(t)
		m.append([EtElEOF()])
		self.t = m

	# This currently is far too simple
	def parse(self, e, t):
		s = e.pop(0)
		n = '}'
		klass = EtElFN
		if s[0]=='/':
			n = '/}'
			s = s[1:]
			klass = EtElReg
		while n not in s:
			s += '{'+e.pop(0)
		p = s.find(n)
		t.append(klass(s[0:p]))
		self.string(e, t, s[p+len(n):])

	def match(self, f):
		state = EtState(self.t)
		for l in f:
			state.step(l)
		state.eof()
		return state.m

class Et(object):
	_template = None

	def __init__(self, file=None, template=None):
		self.template = template
		if file:
			self.read(file)

	@property
	def template(self):
		return self._template

	@template.setter
	def template(self, template):
		self._template	= template
		self._compile	= template and EtCompile(template) or None

	def read(self, name):
		with open(name, 'r') as f:
			self.template = f.read()

	def match_string(self, s):
		return self.match(StringIO(s))

	def match_file(self, name):
		with open(name, 'r') as f:
			return self.match(f)

	def match(self, f):
		"""
		Raises EtNoMatch exception if given file does not match the template.
		Returns list of matches (template parts) found.
		"""
		return self._compile.match(f)

if __name__=='__main__':
	et	= Et(sys.argv[1])
	if len(sys.argv)<=2:
		print(et._compile.t, file=sys.stderr)
		sys.exit(2)
	for name in sys.argv[2:]:
		try:
			n = 0
			for a in et.match_file(name):
				n += 1
				print(name, n, a)
		except EtNoMatch as e:
			print(name, 'err:', e, file=sys.stderr)
			sys.exit(1)
	sys.exit(0)

