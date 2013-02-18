# -*- coding: utf-8 -*-

import wikipedia, re, pprint

def make_translation(template):
	page = wikipedia.Page(wikipedia.getSite('ca'), "Template:"+template)
	text = page.get()
	a = re.findall("\|\s*(.*?)\s*=\s*\{\{\{(.*?)\|\{?\{?\{?(.*?)\|?\}\}\}", text)
	return dict([["(?:"+x[1]+("|"+x[2].replace("{{{","") if x[2] and x[2] != x[1] else "")+")", x[0]] for x in a])

#pprint.pprint( make_translation("cite book") )
book = make_translation("cite book")
book.update({"(?:author2|autor2|coauthors|coauthor|coautors)":"coautors", "editor":"editor", "publication-date":"data", "name": "nom", "editors":"editor"})
trans = make_translation("cite web")
trans.update({"editorial":"editor", "autorlink":u"autorenllaç"})

subs = {'cita web': ['citar web',
              trans],
 'cite book': ['ref-llibre',
               book],
 'cite web': ['citar web',
              trans]}
