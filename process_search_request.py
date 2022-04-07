#!/usr/bin/env python3

import argparse
from bs4 import BeautifulSoup as bs


def get_paragraphs(soup, npar):
	j = 0
	par = [0]*npar
	for i in range(0, npar):
		while soup('p')[j].text == ' ':
			j += 1

		par[i] = soup('p')[j]
		j += 1

	return par


def main(file, npar):
	with open(file,'r') as f:
		content = f.readlines()

	html = content[0]
	soup = bs(html, 'html.parser')
	table = soup('table',{'class':'infobox'})

	for i in table:
		h = i.find_all('tr')
		for j in h:
			heading = j.find_all('th')
			detail = j.find_all('td')
			if heading is not None and detail is not None:
				for x,y in zip(heading,detail):
					print("\033[1m{}\033[0m :: {}".format(x.text,y.text))

	if 'may refer to:' in soup('p')[0].text[-14:]:
		text = soup('p')[0].text
		print(text+'\n')
		body = soup('body')[0]
		sections = body.find_all('h2')
		if len(sections) == 1:
			slist = body.find_all('ul')
			elements = slist[0].find_all('li')
			for element in elements:
				print('\t-'+element.get_text())
		if len(sections) > 1:
			for s,section in enumerate(sections):
				if section.text != 'Navigation menu':
					print('\033[1m'+section.text.replace('[edit]','')+'\033[0m')
					slist = body.find_all('ul')
					elements = slist[s].find_all('li')
					for element in elements:
						print('\t-'+element.get_text())

	elif soup('p')[0].text == 'Other reasons this message may be displayed: ':
		print(soup('p')[0].text[:-2])

	else:
		print('\n')

		npar = min(len(soup('p')), npar)
		paragraphs = get_paragraphs(soup, npar)
		for par in paragraphs:
			bold = par.find_all('b')
			parContent = par.text
			if len(bold) is not 0:
				for i in bold:
					parContent = parContent.replace(i.text,'\033[1m'+i.text+'\033[0m')
			print(parContent+'\n')
			#text = text.replace('<b>','\033[1m')
			#text = text.replace('</b>','\033[0m')
			#soup2 = bs(text, 'html.parser')

			#print(soup2.text)


if __name__=='__main__':
	parser = argparse.ArgumentParser(description='''.''')
	#simulation setup parameters
	parser.add_argument('-f', type=str, default="/tmp/search.txt", help="")
	parser.add_argument('-p', type=int, default="2", help="")
	arg = parser.parse_args()
	main(arg.f,arg.p)
