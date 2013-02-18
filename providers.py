# -*- coding: utf-8 -*-

import sys

class Provider:
	def get(self):
		if len(self.tots) != 0:
			self.last = self.tots.pop(0)
			return self.last
		else:
			return None

	def done(self):
		pass

class ArgumentProvider(Provider):
	def __init__(self):
		self.tots = sys.argv[1:]

class FileProvider(Provider):
	def __init__(self, f):
		self.last = None
		self.f = f
		with open(f) as fi:
			t = fi.read()
		self.tots = t.split("\n")[8:]
		self.fets = open("fets").read().split("\n")

	def done(self):
		if self.last: self.tots.insert(0, self.last)
		#with open("fets"), "w") as fi:
		#	fi.write('\n'.join(self.fets))

class DumpProvider(FileProvider):
	def __init__(self):
		FileProvider.__init__(self, "articlelist")