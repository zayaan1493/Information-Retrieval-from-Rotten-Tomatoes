'''
File Name : the_task.py
Creator : Md Laadla
Roll No. : 20CS60R20
Department : Computer Science and Engineering (MTech, IIT Kharagpur)
Mail Id : mailzayaan1493.ml@kgpian.iitkgp.ac.in
Date : 03-04-2021
Description : The following python code reads cast.html (generated from "the_task.py") and using ply (python lex and yacc) library generates a context free grammar to parse the html and fulfil the user 
			  demands e.g., highest_rated movie, lowest_rated movie, his/her other movie etc..
'''


import re
import ply.lex as lex
import ply.yacc as yacc
import urllib.request, urllib.error, urllib.parse, html


title  = []
year = []
bday = ""
highest_rating = ""
lowest_rating = ""

def cast_crawling():
	#..........................................................LEX..................................................................................................
	# List of token names
	tokens = ('CONTENT',
				'ITEM_VAL_E',
				'ITEM_VAL_S',
				'HIGHEST',
				'LOWEST',
				'BDAY',
				'FILM_S',
				'FILM_E',
				'FILM_TITLE',
				'FILM_YEAR',
				'ROW_S',
				'TAG',
				'COL_E'
				)

	def t_HIGHEST(t):
		r'<p\sclass="celebrity-bio__item"\sdata-qa="celebrity-bio-highest-rated">'
		return t

	def t_LOWEST(t):
		r'<p\sclass="celebrity-bio__item"\sdata-qa="celebrity-bio-lowest-rated">'
		return t

	def t_BDAY(t):
		r'<p\sclass="celebrity-bio__item"\sdata-qa="celebrity-bio-bday">'
		return t

	def t_FILM_S(t):
		r'<tbody\sclass="celebrity-filmography__tbody">'
		return t

	def t_ROW_S(t):
		r'<tr[^>]+>'
		return t


	def t_FILM_TITLE(t):
		r'<td\sclass="celebrity-filmography__title">'
		return  t

	def t_FILM_YEAR(t):
		r'<td\sclass="celebrity-filmography__year">'
		return t
	

	def t_ITEM_VAL_S(t):
		r'<a\sclass="celebrity-bio__link"\shref="[^>]*>'
		return t

	def t_ITEM_VAL_E(t):
		r'</a>'
		return t

	def t_FILM_E(t):
		r'</tbody>'
		return t

	def t_COL_E(t):
		r'</td>'
		return t
	

	def t_CONTENT(t):
		r'([^<^>]+[\s]*)+?'
		return t

	def t_TAG(t):
		r'<(.*?)>'
		return t


	#..................................................................................................

	#ignore white spaces and tabs
	t_ignore  = ' \t'


	# Error handling rule
	def t_error(t):
	    t.lexer.skip(1) 


	# Build the lexer
	lexer = lex.lex(debug=0)


#.............................................................YACC.............................................................................................

	global title,year,bday,highest_rating,lowest_rating
	title  = []
	bday = ""
	highest_rating = ""
	lowest_rating = ""
	year = []



	#.......................The Context Free Grammar................................

	start = 'S'

	def p_S(p):
		'''S : text cast_highest text cast_lowest text cast_bday text table1 text table2 text
		'''

	def p_cast_highest(p):
		'''cast_highest : HIGHEST text ITEM_VAL_S CONTENT ITEM_VAL_E
		                |
		'''
		if len(p)!=1:
			global highest_rating
			highest_rating = p[4].strip()

	def p_cast_lowest(p):
		'''cast_lowest : LOWEST text ITEM_VAL_S CONTENT ITEM_VAL_E
		                |
		'''
		if len(p)!=1:
			global lowest_rating
			lowest_rating = p[4].strip()

	def p_cast_bday(p):
		'''cast_bday : BDAY CONTENT
		             |
		'''
		if len(p)!=1:
			global bday
			k = p[2].split(":")
			bday = "{}: {}".format(k[0].strip(),k[1].strip())


	def p_table1(p):
		'''table1 : FILM_S rows FILM_E
		'''

	def p_rows(p):
		'''rows : rows ROW_S text extra1 text extra2 text
				| ROW_S text extra1 text extra2 text
		'''

	def p_extra1(p):
		'''extra1 : FILM_TITLE TAG CONTENT ITEM_VAL_E COL_E
		          | FILM_TITLE TAG CONTENT TAG COL_E
                  | FILM_TITLE CONTENT COL_E
                  |
		'''
		if len(p)!=1:
			global title_year
			if len(p)==6:
				title.append(p[3].strip())
			elif len(p):
				title.append(p[2].strip())
		else:
			title.append("")

	def p_extra2(p):
		'''extra2 : FILM_YEAR CONTENT COL_E
		          |
		'''
		if len(p)!=1:
			year.append(p[2].strip())
		else:
			year.append("")


	def p_table2(p):
		'''table2 : FILM_S extra3 FILM_E
		          |
		'''

	def p_extra3(p):
		'''extra3 : ROW_S extra3
				  | FILM_TITLE extra3
				  | FILM_YEAR extra3
		          | TAG extra3
				  | CONTENT extra3
				  | ITEM_VAL_E extra3
				  | COL_E extra3
				  |
		'''

	def p_text(p):
		'''text : TAG text
				| CONTENT text
				| ITEM_VAL_E text
                | COL_E text
				| TAG
				| CONTENT
				| ITEM_VAL_E
				| COL_E
                |
		'''

	# Error rule for syntax errors
	def p_error(p):
		pass


	# Build the parser
	parser = yacc.yacc(debug=0)



	#open the file cast.html downloaded by the "the_task.py" file and then crawl the cast page
	file = open("cast.html","r")
	cast_string = file.read()
	cast_string = re.sub('\n',' ',cast_string)
	file.close()

	# file1 = open("file222.txt","w")
	# lexer.input(cast_string)
	# while True:
	# 	tok = lexer.token()
	# 	if not tok:
	# 		break
	# 	print(tok,file = file1)
	# file1.close()


	

	#parser.parse(cast_string) internally makes call to lexer.input(cast_string)
	parser.parse(cast_string)

# cast_crawling()

# print('highest',highest_rating)
# print()
# print('lowest',lowest_rating)
# print()
# print('bday',bday)
# print()
# print('title',title)
# print()
# print(year)

	






