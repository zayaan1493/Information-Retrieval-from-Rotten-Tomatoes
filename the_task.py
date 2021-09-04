'''
File Name : the_task.py
Creator : Md Laadla
Roll No. : 20CS60R20
Department : Computer Science and Engineering (MTech, IIT Kharagpur)
Mail Id : mailzayaan1493.ml@kgpian.iitkgp.ac.in
Date : 03-04-2021
Description : The following python code reads movie.html (generated from movie_extractor) and using ply (python lex and yacc) library generates a context free grammar to parse the html and fulfil the user 
			  demands e.g., movie_name, producer, writers etc..
'''


import re
import ply.lex as lex
import ply.yacc as yacc
import urllib.request, urllib.error, urllib.parse, html
import movie_extractor
import cast_crawler


def movie_crawler():



	#..........................................................LEX..................................................................................................
	# List of token names
	tokens = ('CONTENT',
				'YMAL',
				'LINK_YMAL',
				'WTW',
				'GENRE',
				'ITEM_VAL_GENRE_S',
				'LANGUAGE',
				'PRODUCER',
				'DIRECTOR',
				'WRITER',
				'BOC',
				'RUNTIME',
				'STORYLINE_S',
				'TITLE_S',
				'TITLE_E',
				'TAG',
				'ITEM_VAL_S',
				'ITEM_VAL_E',
				'CAST_LINK',
				'CAST_ACT_S',
				'CAST_MOV_S',
				'CAST_E'
				)
						
	#............................Regular expression rule for each token..................................

	def t_LINK_YMAL(t):
		r'<a\shref="[^"]*"\sclass="recommendations-panel__poster-link">'
		return t

	def t_YMAL(t):
		r'<span\sslot="title"\sclass="recommendations-panel__poster-title">'
		return t

	def t_WTW(t):
		r'<affiliate-icon\s[^>]*></affiliate-icon>'
		return t

	def t_GENRE(t):
		r'<div\sclass="meta-label\ssubtle"\sdata-qa="movie-info-item-label">Genre:</div>'
		return t

	def t_LANGUAGE(t):
		r'<div\sclass="meta-label\ssubtle"\sdata-qa="movie-info-item-label">Original\sLanguage:</div>'
		return t

	def t_DIRECTOR(t):
		r'<div\sclass="meta-label\ssubtle"\sdata-qa="movie-info-item-label">Director:</div>'
		return t

	def t_WRITER(t):
		r'<div\sclass="meta-label\ssubtle"\sdata-qa="movie-info-item-label">Writer:</div>'
		return t

	def t_BOC(t):
		r'<div\sclass="meta-label\ssubtle"\sdata-qa="movie-info-item-label">Box\sOffice\s\(Gross\sUSA\):</div>'
		return t

	def t_RUNTIME(t):
		r'<div\sclass="meta-label\ssubtle"\sdata-qa="movie-info-item-label">Runtime:</div>'
		return t

	def t_STORYLINE_S(t):
		r'<div\sid="movieSynopsis"\sclass="movie_synopsis\sclamp\sclamp-6\sjs-clamp"\sstyle="clear:both"\sdata-qa="movie-info-synopsis">'
		return t


	def t_TITLE_S(t):
		r'<title>'
		return t

	def t_TITLE_E(t):
		r'</title>'
		return t

	def t_PRODUCER(t):
		r'<div\sclass="meta-label\ssubtle"\sdata-qa="movie-info-item-label">Producer:</div>'
		return t

	def t_CAST_LINK(t):
		r'<a\shref="[^"]*"\sclass="unstyled\sarticleLink"\sdata-qa="cast-crew-item-link">'
		return t

	def t_CAST_ACT_S(t):
		r'<span\stitle(.+?)>'
		return t

	def t_CAST_MOV_S(t):
		r'<span\sclass="characters\ssubtle\ssmaller(.+?)>'
		return t

	def t_CAST_E(t):
		r'</span>'
		return t


	def t_ITEM_VAL_GENRE_S(t):
		r'<div\sclass="meta-value\sgenre"\sdata-qa="movie-info-item-value">'
		return t

	def t_ITEM_VAL_S(t):
		r'<div\sclass="meta-value"\sdata-qa="movie-info-item-value">'
		return t

	def t_ITEM_VAL_E(t):
		r'</div>'
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

	#..............................................................................................................................................................


	#re-initialize the values of all the variables for a new movie
	global title,genre,language,producer,runtime,storyline,director,boc,writer,cast,ymal,wtw
	title = ""
	genre = ""
	language =""
	producer = ""
	runtime = ""
	storyline = ""
	director = ""
	boc = ""
	writer = ""
	cast = []
	ymal = {}
	wtw = []


	#.............................................................YACC.............................................................................................


	



	#.......................The Context Free Grammar................................

	start = 'S'

	def p_S(p):
		'''S : text movie_title text movie_like text movie_watch text movie_story text movie_genre text movie_language text movie_director text movie_producer text movie_writer text box_office text movie_runtime text movie_cast text
		'''

	def p_movie_title(p):
		'''movie_title : TITLE_S CONTENT TITLE_E
		'''
		global title
		title = p[2].strip()

	def p_movie_like(p):
		'''movie_like : LINK_YMAL text YMAL CONTENT CAST_E text movie_like
		              | YMAL CONTENT CAST_E text movie_like
		              |
		'''
		if len(p)!=1:
			global ymal
			if len(p)==8:
				ymal[p[4].strip()] = "https://www.rottentomatoes.com"+p[1].split("href")[1].split('"')[1]
			else:
				ymal[p[2].strip()] = ""

	def p_movie_watch(p):
		'''movie_watch : WTW text movie_watch
		               |
		'''
		if len(p)!=1:
			global wtw
			wtw.append(p[1].split("name")[1].split('"')[1])

	


	def p_movie_story(p):
		'''movie_story : STORYLINE_S extra ITEM_VAL_E
		               | 
		'''
		if len(p)!=1:
			global storyline
			storyline = p[2]


	def p_movie_genre(p):
		'''movie_genre : GENRE ITEM_VAL_GENRE_S extra ITEM_VAL_E
		               |
		'''
		if len(p)!=1:
			global genre
			genre = p[3]

	def p_movie_language(p):
		'''movie_language : LANGUAGE ITEM_VAL_S extra ITEM_VAL_E
		                  |
		'''
		if len(p)!=1:
			global language
			language=p[3]

	def p_movie_director(p):
		'''movie_director : DIRECTOR ITEM_VAL_S extra ITEM_VAL_E
		                  |
		'''
		if len(p)!=1:
			global director 
			director = p[3].strip()

	def p_movie_producer(p):
		'''movie_producer : PRODUCER ITEM_VAL_S extra ITEM_VAL_E
		                  |
		'''
		if len(p)!=1:
			global producer
			producer = p[3].strip()

	def p_movie_writer(p):
		'''movie_writer : WRITER ITEM_VAL_S extra ITEM_VAL_E
		                |
		'''
		if len(p)!=1:
			global writer
			writer = p[3].strip()

	def p_box_office(p):
		'''box_office : BOC ITEM_VAL_S CONTENT ITEM_VAL_E
		              |
		'''
		if len(p)!=1:
			global boc
			boc = p[3].strip()


	def p_movie_runtime(p):
		'''movie_runtime : RUNTIME ITEM_VAL_S extra ITEM_VAL_E
		                 |
		'''
		if len(p)!=1:
			global runtime
			runtime = p[3].strip()

	def p_movie_cast(p):
		'''movie_cast : movie_cast text cast1 text cast2
					  | cast1 text cast2
					  |
		'''

	def p_cast1(p):
		'''cast1 : CAST_LINK CAST_ACT_S CONTENT CAST_E
		         | CAST_ACT_S CONTENT CAST_E
		'''
		if len(p)!=1:
			global cast
			if len(p)==5:
				x = p[1].split("href")[1].split('"')[1]
				cast.append("https://www.rottentomatoes.com"+x.strip())
				cast.append(p[3].strip())
			elif len(p)==4:
				
				cast.append("")
				cast.append(p[2].strip())


	def p_cast2(p):
		'''cast2 : CAST_MOV_S TAG extra_cast2 CAST_E
		         | CAST_MOV_S TAG extra_cast3 CAST_E
		'''

	def p_extra_cast2(p):
		'''extra_cast2 : CONTENT TAG
		               | CONTENT
		               |
		'''
		if len(p)!=1:
			if len(p)==3:
				cast.append(p[1].strip())
			elif len(p)==2:
				cast.append(p[1].strip())
		else:
			cast.append("")


	def p_extra_cast3(p):
		'''extra_cast3 : CONTENT TAG CONTENT
		               |
		'''
		if len(p)!=1:
			cast.append(p[1].strip()+'('+p[3].strip()+')')


	def p_extra(p):
		'''extra : TAG extra1
		         | CONTENT
		         |
		'''
		if len(p)!=1:
			if len(p)==3:
				p[0]=p[2]
			elif len(p)==2:
				p[0]=p[1].strip()
		else:
			p[0]=""

	def p_extra1(p):
		'''extra1 : CONTENT TAG extra1
				| CONTENT TAG
				|
		'''
		if len(p)!=1:
			if (len(p)==4):
				p[0]=p[1].strip()+" "+p[3].strip()
			elif (len(p)==3):
				p[0]=p[1].strip()
		else:
			p[0]=""


	def p_text(p):
		'''text : TAG text
				| CONTENT text
				| ITEM_VAL_S text
				| ITEM_VAL_E text
				| CAST_E text
				| TAG
				| CONTENT
				| ITEM_VAL_S
				| ITEM_VAL_E
				| CAST_E
				|
		'''
	#............................................................................


	# Error rule for syntax errors
	def p_error(p):
		pass


	# Build the parser
	parser = yacc.yacc(debug=0)



#..............................................................................................................................................................

	file = open("movie.html","r")
	movie_string = file.read()
	movie_string = re.sub('\n',' ',movie_string)
	file.close()

	# file1 = open("file1.txt","w")
	# lexer.input(movie_string)
	# while True:
	# 	tok = lexer.token()
	# 	if not tok:
	# 		break
	# 	print(tok,file = file1)
	# file1.close()

	#parser.parse(movie_string) internally makes call to lexer.input(movie_string)
	parser.parse(movie_string)



	# print('ymal',ymal)
	# print()
	# print('genre',genre)
	# print()
	# print('director',director)
	# print()
	# print('prod',producer)
	# print()
	# print('Movie name',title)
	# print()
	# print('Writers',writer)
	# print()
	# print('OLang',language)
	# print()
	# print('stroy',storyline)
	# print('bov',boc)
	# print()
	# print('run',runtime)
	# print()
	# i=0
	# while i<len(cast)-2:
	# 	print(cast[i])
	# 	print(cast[i+1])
	# 	print(cast[i+2])
	# 	i+=3
	# print(len(cast))
	# print(*wtw)
	# print()



	#.................Handling user query...............................

	

	title = "-".join(title.split('-')[:-1]).strip()
	
	query_dic = {"1":"Movie Name","2":"Director","3":"Writers","4":"Producer","5":"Original Language",
	"6":"Cast with the character name","7":"Storyline","8":"Box Office Collection",
	"9":"Runtime", "10":"Movie You Might Also Like", "11":"Where to watch"}


	while True:
		print("1. Movie Name\n2. Director\n3. Writers\n4. Producer\n5. Original Language\n6. Cast with the character name\n7. Storyline\n8. Box Office Collection\n9. Runtime\n10. Movie You Might Also Like\n11. Where to watch\n12. Exit")
		query = input("Please select your query : ")
		print()
		result = ""
		if query=='1':
			result=title
		elif query=='2':
			result=director
		elif query=='3':
			result=writer
		elif query=='4':
			result=producer
		elif query=='5':
			result=language
		elif query=='6':
			flag = 1
			while flag:
				i,count=0,1
				print("{}:".format(query_dic[query]))
				print("======================================")
				while i<len(cast)-2:
					result+="{}. {} : ".format(count,cast[i+1])
					x = cast[i+2].split(',')
					for p in range(len(x)):
						if p<len(x)-1:
							result+=x[p].strip()+','
						else:
							result+=x[p].strip()
					print(result)
					count+=1
					result=""
					i+=3
				print("{}. Exit".format(count))
				print("======================================")
				given = input("Select the cast you want to look for:")
				if given.isnumeric():
					if int(given)==count:
						break
					elif 1<=int(given)<count:
						if len(cast[(1+3*(int(given)-1))-1])==0:
							print("No page found for this cast in rottentomatoes")
							continue
						flag = 0

						#get the requested cast and download it as cast.html
						response = urllib.request.urlopen(cast[(1+3*(int(given)-1))-1]) #using arithmetic progression as the for every cast the name, movie_name and the link is present in the single list
						webContent = response.read().decode()
						webContent = html.unescape(webContent)

						f = open("cast"+".html", 'w')
						f.write(webContent)
						f.close()

						#calls the cast_crawler.py python code for crawling the cast
						cast_crawler.cast_crawling()

						cast_dic = {"1":"Highest Rated Film", "2":"Lowest Rated Film", "3":"BirthDay", "4":"His/Her Other Movies"}
						while True:
							print()
							print("=====================================================")
							print("1. Highest Rated Film\n2. Lowest Rated Film\n3. BirthDay\n4. His/Her Other Movies\n5. Exit")
							print("=====================================================")
							get = input("Please select the option of your choice from above:")
							if get.isnumeric():
								if int(get)==5:
									break
								elif 1<=int(get)<5:
									if get=='1':
										print("{}--> {}".format(cast_dic[get],cast_crawler.highest_rating))
									elif get=='2':
										print("{}--> {}".format(cast_dic[get],cast_crawler.lowest_rating))
									elif get=='3':
										print("{}".format(cast_crawler.bday))
									elif get=='4':
										y = "okay"
										while not y.isnumeric():
											y = input("Provide a valid year:")
										print("Movies in and after {} :".format(y))
										print("-------------------------------------------------------")
										for name,yr in zip(cast_crawler.title,cast_crawler.year):
											if int(y)<=int(yr):
												print("{}-->{}".format(name,yr))
											else:
												break
										print("-------------------------------------------------------")
								else:
									print("Please enter valid number")
							else:
								print("Please enter valid number")




						# print('highest',cast_crawler.highest_rating)
						# print()
						# print('lowest',cast_crawler.lowest_rating)
						# print()
						# print('bday',cast_crawler.bday)
						# print()
						# print('title_year',cast_crawler.title_year)
						# print()
						# print(len(cast_crawler.title_year))


					else:
						print("Please enter valid number")
				else:
					print("Please enter valid number")



		elif query=='7':
			result=storyline
		elif query=='8':
			result=boc
		elif query=='9':
			result=runtime
		elif query=='10':
			flag=1
			while flag:
				count = 1
				ymal_count={}
				print("========================================")
				for i in ymal.keys():
					print("{}. {}".format(count,i))
					ymal_count[str(count)]=i
					count+=1
				print("{}. Exit".format(count))
				print("========================================")
				x=input("Select the movie you want to look for:")

				if x.isnumeric():
					if int(x)==count:
						break
					elif 1<=int(x)<count:
						if len(ymal[ymal_count[x]])==0:
							print("Movie Page not found in rottentomatoes")
							continue
						flag = 0

						#download the movie.html file for further crawling
						response = urllib.request.urlopen(ymal[ymal_count[x]])
						webContent = response.read().decode()
						webContent = html.unescape(webContent)

						f = open("movie"+".html", 'w')
						f.write(webContent)
						f.close()

						#crawl the movie recursively
						movie_crawler()
						return
					else:
						print("Please enter valid number")
				else:
					print("Please enter valid number")

		elif query=='11':
			print(query_dic[query]+" :")
			for i in wtw:
				print(i)

		elif query=='12':
			break
		else:
			print("Please enter valid query number")
			print()
			continue

		if query!='6' and query!='7' and query!='11' and query!='10':
			result=result.strip()
			print("{}:\n{}".format(query_dic[query],result))
			
		# elif query=='6':
		# 	final_result = result.split("<>")
		# 	final_result.pop()
		# 	print("{}:".format(query_dic[query]))
		# 	for x in final_result:
		# 		print(x.strip())
				
		elif query=='7':
			print("{}:\n{}".format(query_dic[query],result))
			
		print()
		








#.....................................the main function.................................................

print("Welcome to the movie infromation extractor wizard!!!")



while (True):


	step=input("Kindly press\n1. To continue your search for a new movie\n2. To exit\n")

	if (step=='1'):
		#the movie_extractor.py file imported in this file, downloads the movie.txt
		movie_extractor.my_function()

		#intialising the data structures needed to do our query task
		title = ""
		genre = ""
		language =""
		producer = ""
		runtime = ""
		storyline = ""
		director = ""
		boc = ""
		writer = ""
		cast = []
		ymal = {}
		wtw = []

		#calls the movie_crawler funtion to crawl the movie.html
		movie_crawler()

	elif step=='2':
		break

	else:
		print("Wrong input")

#......................................................................................................
