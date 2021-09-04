'''
File Name : movie_extractor.py
Creator : Md Laadla
Roll No. : 20CS60R20
Department : Computer Science and Engineering (MTech, IIT Kharagpur)
Mail Id : mailzayaan1493.ml@kgpian.iitkgp.ac.in
Date : 03-04-2021
Description : From the given genre list the following python code asks the user to select a genre and prints 100 top movies from the selected genre and then prompts the user to select one movie from
              the movie list and saves the selected movie as "movie.html"
'''


import urllib.request, urllib.error, urllib.parse, html, re

def my_function():

  

  '''genre_links --> a dictionary where key is a number representing the genre and the value is the link of the genre
     genre_key   --> a dictionary where the key is a number representing the genre and the value is the name of the genre
     movie_links --> a dictionary where the key is the name of the movie and the value is the link of the corresponding movie
     movie_count_map --> a dictinary where the key is a number representing the movie and the value is the name of the movie'''
  genre_links={'1': 'https://www.rottentomatoes.com/top/bestofrt/top_100_action__adventure_movies/',
   '2': 'https://www.rottentomatoes.com/top/bestofrt/top_100_animation_movies/',
   '3': 'https://www.rottentomatoes.com/top/bestofrt/top_100_drama_movies/',
   '4': 'https://www.rottentomatoes.com/top/bestofrt/top_100_comedy_movies/',
   '5': 'https://www.rottentomatoes.com/top/bestofrt/top_100_mystery__suspense_movies/',
   '6': 'https://www.rottentomatoes.com/top/bestofrt/top_100_horror_movies/',
   '7': 'https://www.rottentomatoes.com/top/bestofrt/top_100_science_fiction__fantasy_movies/',
   '8': 'https://www.rottentomatoes.com/top/bestofrt/top_100_documentary_movies/',
   '9': 'https://www.rottentomatoes.com/top/bestofrt/top_100_romance_movies/',
   '10': 'https://www.rottentomatoes.com/top/bestofrt/top_100_classics_movies/'}
  genre_key={'1':"Action & Adventure",
            '2':"Animation",
            '3':"Drama",
            '4':"Comedy",
            '5':"Mystery & Suspense",
            '6':"Horror",
            '7':"Sci-Fi",
            '8':"Documentary",
            '9':"Romance",
            "10":"Classics"}



  print("============================================")
  print("1. Action & Adventure\n2. Animation\n3. Drama\n4. Comedy\n5. Mystery & Suspense\n6. Horror\n7. Sci-Fi\n8. Documentary\n9. Romance\n10. Classics")
  print("============================================")

  while True:
    user_genre = input("Select the genre of your choice from above: ")

    if user_genre.isnumeric():

      if 0<int(user_genre)<11:
        break
      else:
        print("Wrong Input!")
        continue

    else:
      print("Wrong Input!")
      continue


  genre = genre_key[user_genre]


  movie_links={}
  print("Here is the list of top 100 {} movies:".format(genre))
  print()
  count=1
  movie_count_map={}
  with urllib.request.urlopen(genre_links[user_genre]) as response:
      string = response.read().decode('utf-8')
      string = html.unescape(string)
      
      #Error handling such that atleast one table is there in the html file else not possible to get the list of movies
      n_table = re.split(r'<table class="table">', string)
      if (len(n_table)<2):
          print("Error : No table is present in the html file")
          exit()
      #get the index of the string(html text converted into string) from where the table starts
      st = re.search(r'<table class="table">', string).start()
      
      #get the index of the end of the table. To search efficiently we start our search from the index after the table start tag
      end = re.search('</table>',string[st:]).start()+st
      
      #remove all new lines to spaces
      string = re.sub('\n',' ',string[st:end])

      #split the table to get each row
      rows = re.split('<tr>',string)
      
      #We now iterate each row
      new_rows=[]
      for r in rows[2:]:
          new_rows.append(re.split('</tr>',r)[0])
          
      #Get the third column and also <a> tag is only present in this column
      for r in new_rows:
          rx = re.split('<td[^<]*>',r)

          m = re.split('</td>',rx[3])[0] #since the third column contains the name of the movie and its link and also here we remove the column tag end i.e, </td>

          m = re.split('</a>',m)[0] #removing the ending tag </a>

          m = re.split('>',m) #split on '>' to get the name of the movie as well as the link in a list of string

          link = m[0].split() #to get the href of the tag in order to get the link eventually

          link = link[1].split('"')[1]

          movie_name = m[1].strip()
          movie_count_map[str(count)]=movie_name
          print("{}. {}".format(count,movie_name))
          movie_links[movie_count_map[str(count)]]="https://www.rottentomatoes.com"+link
          count+=1


  while True:
    name = input("\nEnter the movie number of your choice: ")

    if name.isnumeric():
      if 0<int(name)<101:
        break
      else:
        print("Wrong Input!")
        continue

    else:
      print("Wrong Input!")
      continue

  # open the link of the movie and write the html file in "movie.html"
  response = urllib.request.urlopen(movie_links[movie_count_map[name]])
  webContent = response.read().decode()
  webContent = html.unescape(webContent)

  f = open("movie"+".html", 'w')
  f.write(webContent)
  f.close()