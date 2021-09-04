This project is on crawling and scrapping web pages and extracting the required information from them by creating suitable grammar rules.

Task 1 (Crawling RottenTomatoes website):
1. RottenTomatoes is an IMDb like website, where we can find an online database of information related to films, television programs, including cast, production crew, personal biographies, plot summaries, trivia, ratings, critic and fan reviews.

2. I have assumed that I am given a file named “rotten tomatoes movie genre link.txt,” which contains
URL links for ten different genre-wise top 100 movie lists.

3. A python code is written that reads each of the URLs, saves the pages in HTML format.

4. Now given a user input of any of the ten genres, the task is to list all the movies in that list
and wait for user input of a particular movie name from the list.

5. Given a movie name as the input, the code downloads and save the corresponding
movie page’s HTML file.


Task 2 (Creating grammar and parsing the files):
1. After saving movie pages in HTML format, I have studied the syntax of HTML files.

2. Created a grammar that can be used to extract the following fields for the movies.
● Movie Name
● Director
● Writers
● Producer
● Original Language
● Cast with the character name
● Storyline
● Box Office Collection
● Runtime

Along with the above information, the code tries to give the user the following information: 
● YOU MIGHT ALSO LIKE - Similar kind of movie suggestions 
● WHERE TO WATCH - Online platforms where the movie can be seen. 
 
So if user input is <YOU MIGHT ALSO LIKE>, then the code prints the similar movies with 
<Movie X>, and wait for user input from the listed movies and again present the same options 
list. 
 
Similarly for the sake of completion, if user input is <WHERE TO WATCH>, then the code 
prints the available online platforms where the movie is streaming. 

I have also expanded the cast member functionality for a movie in the below way: 
Given a movie and user input for a cast member, after printing all of its cast members, the code waits for user input of any one of the listed cast member, given the input the code downloads and saves that actor/actress profile and the grammar is written using PLY to extract the below fields: 
● Highest Rated film 
● Lowest Rated film 
● Birthday 
● His/Her other movies 
Then the code waits for the user to select from any of the above options and show the result as per 
selection and for the ‘His/Her other movies’ further the code asks for a year and use it as a filter to show all the movies on or after that year.

4. A python code is designed to extract the above fields. The program shows all the possible query fields a user can ask for(from the above list items). And according to the user selection, it shows the corresponding field for the particular movie or move to the movie or cast according to the selection of the user ("you might also like" or "Cast and Crew") and again does the same work for a movie or cast chosen by the user as mentioned above.

5. The program also saves the result in a log file as per the following format.
<Genre> <Movie_name> <Field_requested> <Field_value>
For a field with multiple values, it should make an entry for each value.

6. Note that in this project I haven't  use the “Beautiful Soup” python package. The entire code is based on the PLY package of python.

