# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import providers
from subs import subs
import wikipedia
import re
import atexit

SITE = wikipedia.getSite('ca')

def get_template_params(name):
	page = wikipedia.Page(SITE, "Template:"+name)
	text = page.get()
	return set(re.findall("\{\{\{(.*?)(?:\||\}\}\})", text))

tmp = get_template_params("citar web")
allowed = {"cite web": tmp, "cita web": tmp, "cite book": get_template_params("ref-llibre")}

def get_templates(text):
	tots = []

	prev = ""
	current = ""
	opened = 0
	for char in text:
		if char == "{" and prev == "{":
			opened += 1
			if opened == 1:
				char += "{"
		elif char == "}" and prev == "}":
			opened -= 1
			prev = "<INUTIL>"
			if opened == 0:
				tots.append(current+"}")
				current = ""
				continue
		if opened != 0:
			current += char
		prev = char
	return tots

def get_template_name(template):
	a = re.findall("\{\{\s*(.+?)\s*\|", template, re.S|re.MULTILINE)
	if len(a) == 0:
		a = re.findall("\{\{\s*(.+?)\}\}", template, re.S|re.MULTILINE)
	return a[0]

def get_from_dict(dicc, element, name=None):
	for e,v in sorted(dicc.iteritems(), key=lambda x: len(x[0]), reverse=True):
		if re.search("^"+e+"$", element, flags=re.IGNORECASE):
			return re.sub("^"+e+"$", v, element, flags=re.IGNORECASE)
	print ("(ok)" if element in allowed[name.lower()] else "    "), element, "@<"+name+">"
	if element in allowed[name.lower()]: return element
	else: return False

def replace(template, dicc, name):
	template = template.rstrip()
	args = re.split("\s*\|\s*", template)
	t = "{{"+dicc[0]

	editorfirst = None
	editorlast = None
	editordone = False

	append = {"middle":"nom", "subtitle":u"títol"}
	toappend = {"nom":"", u"títol": ""}

	for arg in args[1:]:
		sp = re.split("\s*=\s*", arg)
		if sp[0] in append:
			toappend[append[sp[0]]] = sp[1]

	delete = ["deadurl","author2-link"]
	for arg in args[1:]:
		sp = re.split("\s*=\s*", arg)
		if sp[0] == "editor1-first" or sp[0] == "editor-first":
			editorfirst = sp[1]
			continue
		elif sp[0] == "editor1-last" or sp[0] == "editor-last":
			editorlast = sp[1]
			continue
		elif sp[0] == "editor":
			editordone = True
		elif sp[0] in delete:
			continue
		if sp[0] in append.keys(): continue
		if len(sp) == 2:
			if sp[1] == "" and sp[0] not in ["nom", "cognom", u"títol", "lloc","editorial", "data","isbn","consulta","url"]: continue
			got = get_from_dict(dicc[1], sp[0], name)
			if not got:
				#print "MOC MOC error"
				return False
			t += " | "+got+"="+sp[1]+(" "+toappend[got] if got in toappend and toappend[got] else "")
		else:
			if arg.lstrip().rstrip() == "": continue
			t += " | "+arg.rstrip().lstrip()
	t = t[:-2]
	if not editordone and editorfirst and editorlast:
		t += " | editor="+editorlast+", "+editorfirst
	t += "}}"
	return t

def do(title):
	print " --",title,"-- "
	page = wikipedia.Page(SITE, title)
	vell = text = page.get()
	templates = get_templates(text)
	for template in templates:
		name = get_template_name(template)
		if name.lower() in subs:
			replaced = replace(template, subs[name.lower()], name)
			if not replaced: return False
			text = text.replace(template, replaced)

	#wikipedia.showDiff(vell, text)
	pass#page.put(text, comment=u'Robot tradueix i formateja referències [beta]')
	return title

def main():
	args = sys.argv[1:]
	if args[0] == "-bl":
		provider = providers.BackLinkProvider()
	elif args[0] == "-dump":
		provider = providers.DumpProvider()
	elif args[0] == "-file":
		provider = providers.FileProvider(args[1])
	else:
		provider = providers.ArgumentProvider()

	atexit.register(provider.done)

	while True:
		e = provider.get()
		if not e:
			break
		if e in provider.fets: continue
		res = do(e)
		if res: provider.fets.append(res)
		provider.last = None

main()