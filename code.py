#!/usr/bin/env python

import web, config, view, sys, urllib, csv, os.path
from view import render
from lxml.html import ElementSoup
from xml.dom.minidom import Document

urls = (
    '/freyrhelp/', 'index',
	'/freyrhelp/companies', 'companies'
)

class companies:

	EXCHANGE_MAP = {'CSE': 'CO',
					'STO': 'ST',
					'HEL': 'HE',
					'ISE': 'IC'}

	CURRENCY_MAP = {'CSE': 'DKK',
					'STO': 'SEK',
					'HEL': 'EUR',
					'ISE': 'ISK'}

	def append_child(self, doc, elem, name, value):
		n = doc.createElement(name)
		v = doc.createTextNode(value)
		n.appendChild(v)
		elem.appendChild(n)

	def GET(self):

		# list found at http://omxnordicexchange.com/kursinformation/Aktier/analysevarktoj/
		filename = os.path.join(os.path.dirname(__file__), 'aktier.csv')
		reader = csv.reader(open(filename), delimiter=',')

		doc = Document()
		res = doc.createElement('companies')
		doc.appendChild(res)

		for row in reader:
			if not len(row[6]) > 10:
				continue

			# name, currency, exchange, size, sector, symbol, se_number = row

			symbol = row[5].strip().split(' ')

			if len(symbol) > 1:
				symbol = symbol[0].upper() + symbol[1].lower()
			else:
				symbol = symbol[0].upper()

			exchange = row[2].strip().upper()
			currency = row[1].strip().upper()

			extra = ''
			if self.CURRENCY_MAP[exchange] != currency:
				symbol = symbol + currency
				extra = 'p'

			symbol = symbol + '.' + self.EXCHANGE_MAP[exchange] + extra

			company = doc.createElement('company')

			self.append_child(doc, company, 'name', row[0].strip())
			self.append_child(doc, company, 'currency', row[1].strip())
			self.append_child(doc, company, 'exchange', row[2].strip())
			self.append_child(doc, company, 'size', row[3].strip())
			self.append_child(doc, company, 'sector', row[4].strip())
			self.append_child(doc, company, 'symbol', row[5].strip())
			self.append_child(doc, company, 'isin', row[6].strip())
			self.append_child(doc, company, 'reuters-symbol-guess', symbol)

			res.appendChild(company)

		print doc.toprettyxml(indent="  ")

class index:
	def GET(self):
		q = web.input(url=None, xpath=None)

		result = ''

		if q.url and q.xpath:
			result = self.query(q.url, q.xpath)
		
		print render.index(result, q)

	def query(self, url, xpath):
		doc = ElementSoup.parse(urllib.urlopen(url))
		elem = doc.xpath(xpath)
		print "elems found = %d<br />" % len(elem)
		for e in elem:
			print "found: %s<br />" % e.text
			
		if elem is None or len(elem) == 0:
			return None
		else:
			return elem[0].text

if __name__ == "__main__":
    web.run(urls, globals(), *config.middleware)
