### Best Matched Restaurants

#### Introduction

This project is to provide a simple search service to a local area given particular criteria.

1. Provide user up to five parameters to perform a search (query and filter queries)
2. If invalid parameter value is given, return an error message.
3. If no matches found, return an empty list. If less than 5 matches, return entire result set. If more than 5, take the top 5.
4. The Best Match is Restaurant Name -> Distance (closest) > Customer Rating (Highest) > Price (Lowest).

### Assumptions

Here I will lay out the assumptions on tackling the assignment.
1. Use of outside modules such as numpy, pandas, levenshtein and jaro modules was allowed.
2. There were two names in the dataset that appeared unusual so I renamed thosed restaurant names. 
3. Since most of the documents are either uni-grams and bi-grams, I decided to use simpler distance metrics for comparing string instead of TF-IDF or BM25 due to observed poor performance.
4. When a query is issued to the dataframe, filter queries are processed before and then the query is issued for the search.

### Operation procedure.

1. There is requirements.txt file included in the list of files. Create a virtual environment using the requirements.txt
2. Run python script "searchExec.py"
3. Select the search metric to be used for search (Levenshtein or Jaro-Winkler)
4. Follow the instructions as show in the printed statements.
5. Enter the query in the following format: "query,distance,customer_rating,price,cuisine"
6. View printed results  
7. Program will ask if you want to issue another query or exit the program. 
