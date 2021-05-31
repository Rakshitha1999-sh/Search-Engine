"""
File: searchengine.py
---------------------
Implementing a text-based version of a search engine (Google, Bing, Baidu, etc.)! 
"""


import os
import sys
import string


def create_index(filenames, index, file_titles):
    """
    This function is passed:
        filenames:      a list of file names (strings)

        index:          a dictionary mapping from terms to file names (i.e., inverted index)
                        (term -> list of file names that contain that term)

        file_titles:    a dictionary mapping from a file names to the title of the article
                        in a given file
                        (file name -> title of article in that file)

    The function will update the index passed in to include the terms in the files
    in the list filenames.  Also, the file_titles dictionary will be updated to
    include files in the list of filenames.

    >>> index = {}
    >>> file_titles = {}
    >>> create_index(['test1.txt'], index, file_titles)
    >>> index
    {'file': ['test1.txt'], '1': ['test1.txt'], 'title': ['test1.txt'], 'apple': ['test1.txt'], 'ball': ['test1.txt'], 'carrot': ['test1.txt']}
    >>> file_titles
    {'test1.txt': 'File 1 Title'}
    >>> index = {}
    >>> file_titles = {}
    >>> create_index(['test2.txt'], index, file_titles)
    >>> index
    {'file': ['test2.txt'], '2': ['test2.txt'], 'title': ['test2.txt'], 'ball': ['test2.txt'], 'carrot': ['test2.txt'], 'dog': ['test2.txt']}
    >>> file_titles
    {'test2.txt': 'File 2 Title'}
    >>> index = {}
    >>> file_titles = {}
    >>> create_index(['test1.txt', 'test2.txt'], index, file_titles)
    >>> index
    {'file': ['test1.txt', 'test2.txt'], '1': ['test1.txt'], 'title': ['test1.txt', 'test2.txt'], 'apple': ['test1.txt'], 'ball': ['test1.txt', 'test2.txt'], 'carrot': ['test1.txt', 'test2.txt'], '2': ['test2.txt'], 'dog': ['test2.txt']}
    >>> index = {}
    >>> file_titles = {}
    >>> create_index(['test1.txt', 'test2.txt', 'test2.txt'], index, file_titles)
    >>> index
    {'file': ['test1.txt', 'test2.txt'], '1': ['test1.txt'], 'title': ['test1.txt', 'test2.txt'], 'apple': ['test1.txt'], 'ball': ['test1.txt', 'test2.txt'], 'carrot': ['test1.txt', 'test2.txt'], '2': ['test2.txt'], 'dog': ['test2.txt']}
    >>> file_titles
    {'test1.txt': 'File 1 Title', 'test2.txt': 'File 2 Title'}
    >>> index = {'file': ['test1.txt'], '1': ['test1.txt'], 'title': ['test1.txt'], 'apple': ['test1.txt'], 'ball': ['test1.txt'], 'carrot': ['test1.txt']}
    >>> file_titles = {'test1.txt': 'File 1 Title'}
    >>> create_index([], index, file_titles)
    >>> index
    {'file': ['test1.txt'], '1': ['test1.txt'], 'title': ['test1.txt'], 'apple': ['test1.txt'], 'ball': ['test1.txt'], 'carrot': ['test1.txt']}
    >>> file_titles
    {'test1.txt': 'File 1 Title'}
    """
    
    #Building the index

    for file in filenames:
        f=open(file)
        #tracks the number of lines in a file
        file_line_count=0
        
        for line in f:

            #Building file_titles

            #check if line is the title of the file
            if file_line_count==0:
                
                line=line.strip()
                title_line=line.strip(string.punctuation)

                #Adding title of the file to the key filename
                file_titles[file]=title_line

            #extracting each term from a line into a list
            terms=line.split()
            
            for term in terms:
                #removing punctuation marks at the start and end of the term
                term=term.strip(string.punctuation)
                
                if term.isalnum():
                    #check if the term is a word or a number
                    if term.isalpha():
                        term=term.lower()
                    
                    if term not in index:
                        #add the term as a key in index    
                        index[term]=[]
                    
                    #add the filename to the key term
                    if file not in index[term]:
                        index[term].append(file)
            
            file_line_count+=1
        
        f.close()


def search(index, query):
    """
    This function is passed:
        index:      a dictionary mapping from terms to file names (inverted index)
                    (term -> list of file names that contain that term)

        query  :    a query (string), where any letters will be lowercase

    The function returns a list of the names of all the files that contain *all* of the
    terms in the query (using the index passed in).

    >>> index = {}
    >>> create_index(['test1.txt', 'test2.txt'], index, {})
    >>> search(index, 'apple')
    ['test1.txt']
    >>> search(index, 'ball')
    ['test1.txt', 'test2.txt']
    >>> search(index, 'file')
    ['test1.txt', 'test2.txt']
    >>> search(index, '2')
    ['test2.txt']
    >>> search(index, 'carrot')
    ['test1.txt', 'test2.txt']
    >>> search(index, 'dog')
    ['test2.txt']
    >>> search(index, 'nope')
    []
    >>> search(index, 'apple carrot')
    ['test1.txt']
    >>> search(index, 'apple ball file')
    ['test1.txt']
    >>> search(index, 'apple ball nope')
    []
    """

    #creating an empty list to store the filenames 
    #containing all the terms of the query
    posting_list=[]
    
    #extracting each term in a query
    query=query.strip()
    query=query.strip(string.punctuation)
    query=query.split()

    #extracting the appearance of first term in query in files
    term=query[0]
    term=term.strip(string.punctuation)
    if term in index:
        posting_list=index[term]

    #looping over rest of the terms in the query to get the 
    #list of common files which contain all the terms in the query
    for i in range(1,len(query)):
        new_posting_list=[]
        term=query[i]
        term=term.strip(string.punctuation)
        if term in index:
            new_posting_list=index[term]

        #obtain common filenames which has both the terms
        posting_list=common(posting_list,new_posting_list)

    return posting_list


def common(list1, list2):
    """
    This function is passed two lists and returns a new list containing
    those elements that appear in both of the lists passed in.
    >>> common(['a'], ['a'])
    ['a']
    >>> common(['a', 'b', 'c'], ['x', 'a', 'z', 'c'])
    ['a', 'c']
    >>> common(['a', 'b', 'c'], ['x', 'y', 'z'])
    []
    >>> common(['a', 'a', 'b'], ['a', 'a', 'x'])
    ['a']
    """
    #create an empty list to store the common elements
    common_list=[]

    #loop over all elements of list1
    for element_1 in list1:

        #loop over all elements of list2
        for element_2 in list2:

            if element_1==element_2:
                #extracting the common element
                common_element=element_1

                #checking if the common_element is already present in the common_list
                if common_element not in common_list:
                    common_list.append(common_element)

    return common_list


##### YOU SHOULD NOT NEED TO MODIFY ANY CODE BELOW THIS LINE (UNLESS YOU'RE ADDING EXTENSIONS) #####


def do_searches(index, file_titles):
    """
    This function is given an inverted index and a dictionary mapping from
    file names to the titles of articles in those files.  It allows the user
    to run searches against the data in that index.
    """
    while True:
        query = input("Query (empty query to stop): ")
        query = query.lower()                   # convert query to lowercase
        if query == '':
            break
        results = search(index, query)

        # display query results
        print("Results for query '" + query + "':")
        if results:                             # check for non-empty results list
            for i in range(len(results)):
                title = file_titles[results[i]]
                print(str(i + 1) + ".  Title: " + title + ",  File: " + results[i])
        else:
            print("No results match that query.")


def textfiles_in_dir(directory):
    """
    DO NOT MODIFY
    Given the name of a valid directory, returns a list of the .txt
    file names within it.

    Input:
        directory (string): name of directory
    Returns:
        list of (string) names of .txt files in directory
    """
    filenames = []

    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            filenames.append(os.path.join(directory, filename))

    return filenames


def main():
    """
    Usage: searchengine.py <file directory> -s
    The first argument specified should be the directory of text files that
    will be indexed/searched.  If the parameter -s is provided, then the
    user can interactively search (using the index).  Otherwise (if -s is
    not included), the index and the dictionary mapping file names to article
    titles are just printed on the console.
    """
    # Get command line arguments
    args = sys.argv[1:]

    num_args = len(args)
    if num_args < 1 or num_args > 2:
        print('Please specify directory of files to index as first argument.')
        print('Add -s to also search (otherwise, index and file titles will just be printed).')
    else:
        # args[0] should be the folder containing all the files to index/search.
        directory = args[0]
        if os.path.exists(directory):
            # Build index from files in the given directory
            files = textfiles_in_dir(directory)
            index = {}          # index is empty to start
            file_titles = {}    # mapping of file names to article titles is empty to start
            create_index(files, index, file_titles)

            # Either allow the user to search using the index, or just print the index
            if num_args == 2 and args[1] == '-s':
                do_searches(index, file_titles)
            else:
                print('Index:')
                print(index)
                print('File names -> document titles:')
                print(file_titles)
        else:
            print('Directory "' + directory + '" does not exist.')


if __name__ == '__main__':
    main()
