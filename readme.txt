IMPLEMENTING A TEXT BASED VERSION OF SEARCH ENGINE(GOOGLE,BING,BAIDU etc.) GIVEN A SET OF TEXT FILES AND A QUERY AS INPUT.


*) create_index(filenames, index, file_titles) to read in a list of filenames and update an index of 
which terms show up in which files, as well as a file titles dictionary that maps the filename to its title.
Most search engines are built on top of an "inverted index", or "index" for short -- an index is a structure where, 
for each term, we have a list of documents that this term appears in. 

*) Consider the following examples of terms and documents they appear in:
"burrito" appears in the text document "recipes.txt", "greatest eats.txt", "top 10 foods.txt", and "favs.txt"
"sushi" appears in the text document "favs.txt" and "Japanese foods.txt"
"samosa" appears in the text document "appetizers.txt"

*) The most natural structure to use in Python to represent such a mapping from terms to a list of documents is a dictionary. 
The above index could be represented as the following dictionary with keys that are strings and values that are lists of strings:

index = {
    'burrito': ['recipes.txt', 'greatest eats.txt', 'top 10 foods.txt', 'favs.txt'],
    'sushi': ['favs.txt', 'Japanese foods.txt'],
    'samosa': ['appetizers.txt']
}

*) create_index(filenames, index, file_titles is passed the following information:

filenames: filenames is a list of file names (strings) that you'll use to build an index.
index: indes is a dictionary representing the index that you'll build up. When your function is called, 
it will be passed an empty dictionary ({}) for index. Since dictionaries are mutable types, 
any changes your function makes to index will persist after the function completes; 
there's no need to return anything.
file_titles: is a dictionary where the keys are file names (strings) and the 
values are the titles of the articles in each file (also strings). 


*) If we started with an empty index before processing the file doc1.txt, 
after processing doc1.txt the index should look like this:

{
    'we': ['doc1.txt'],
    'are': ['doc1.txt'],
    '100,000': ['doc1.txt'],
    'strong': ['doc1.txt']
}

Let's say that after processing doc1.txt, 
we process another file, doc2.txt, which is shown below:

Strong, you are!
--Yoda--
We should appropriately update the index we had 
before with the terms in doc2.txt to result in index as below:

{
    'we': ['doc1.txt'],
    'are': ['doc1.txt', 'doc2.txt'],
    '100,000': ['doc1.txt'],
    'strong': ['doc1.txt', 'doc2.txt'],
    'you': ['doc2.txt'],
    'yoda': ['doc2.txt']
}


*) Here's an example of the first portion of two of the actual files (001.txt and 002.txt , respectively) 
in the BBC News article data 

001.txt

Broadband steams ahead in the US

More and more Americans are joining the internet's fast lane, according to official figures.
...
002.txt

EA to take on film and TV giants

Video game giant Electronic Arts (EA) says it wants to become the biggest entertainment firm in the world.
...
If file_titles starts as an empty dictionary (which is the case when create_index() is called), 
after we process 001.txt and 002.txt, the file_titles dictionary should look like this:

{
    '001.txt': 'Broadband steams ahead in the US',
    '002.txt': 'EA to take on film and TV giants',
}

*) search(index, query) should return a list of the names of the files that contain all the terms in the given query. 
This list of files is called the "posting list" for the term.
his function is passed the following parameters:
index: index is the index produced by your create_index() function
query: query is a string representing the user's query.


*) Here's the output of a working program running on some sample 
queries on the BBC News data:

Query (empty query to stop): stanford
Results for query 'stanford':
1. Title: Yahoo celebrates a decade online, File: bbcnews/066.txt 
2. Title: Google to scan famous libraries, File: bbcnews/217.txt 
Query (empty query to stop): bike
Results for query 'bike':
1. Title: Games help you 'learn and play', File: bbcnews/291.txt 
2. Title: The Force is strong in Battlefront, File: bbcnews/339.txt 
Query (empty query to stop): stanford bike
Results for query 'stanford bike':
No results match that query.
Query (empty query to stop): windows virus security patch
Results for query 'windows virus security patch':
1. Title: Microsoft releases patches, File: bbcnews/003.txt
2. Title: Microsoft releases bumper patches, File: bbcnews/162.txt 
Query (empty query to stop): cheap apple products
Results for query 'cheap apple products':
1. Title: Apple Mac mini gets warm welcome, File: bbcnews/033.txt 
Query (empty query to stop): *user presses "enter" to end program*

