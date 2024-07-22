import csv
import re
from collections import defaultdict, Counter
from fuzzywuzzy import process, fuzz
from nltk.corpus import stopwords

# Ensure we have the necessary NLTK data files
import nltk
nltk.download('stopwords', quiet=True)

# Read and parse the CSV data
def read_csv(file_path):
    movies = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            movies.append(row)
    return movies

# Normalize and tokenize text
def normalize(text):
    text = text.lower()
    text = re.sub(r'\W+', ' ', text)
    return text.strip().split()

# Build the inverted index
def build_inverted_index(movies):
    # Load a set of English stop words to exclude from full-text search indexing
    stop_words = set(stopwords.words('english'))
    
    # Initialize a nested defaultdict for storing movie indices by different attributes
    index = defaultdict(lambda: defaultdict(set))
    
    # Initialize separate indexes for actors and directors to prevent role confusion
    index['actor'] = defaultdict(set)
    index['director'] = defaultdict(set)
    
    # Initialize a nested defaultdict for storing term frequencies in movie descriptions
    term_frequency = defaultdict(lambda: defaultdict(Counter))
    
    # Initialize a set to store unique names of all persons (cast and directors)
    person_name_set = set()
    
    # Process each movie in the provided list
    for movie in movies:
        # Extract relevant fields from each movie dictionary
        title = movie['name']
        year = movie['year']
        rating = movie['rating']
        genre = movie['genre']
        certificate = movie['certificate']
        cast = movie['casts'].split(',')
        directors = movie['directors'].split(',')
        
        # Index movies by title, converting title to lowercase for case-insensitive matching
        index['title'][title.lower()].add(title)
        # Index movies by year
        index['year'][year].add(title)
        # Index movies by rating
        index['rating'][rating].add(title)
        # Index movies by certificate
        index['certificate'][certificate].add(title)
        
        # Index movies by genre, splitting genres by comma and stripping extra spaces
        for g in genre.split(','):
            index['genre'][g.strip().lower()].add(title)
        
        # Index each actor by name, store in lowercase
        for actor in cast:
            actor = actor.strip().lower()
            index['actor'][actor].add(title)
            person_name_set.add(actor)
        
        # Index each director by name, store in lowercase
        for director in directors:
            director = director.strip().lower()
            index['director'][director].add(title)
            person_name_set.add(director)
        
        # Prepare for full-text search index
        # Combine all textual information into a single string
        all_text = f"{title} {year} {rating} {genre} {certificate} {' '.join(cast)} {' '.join(directors)}"
        # Normalize the text, remove stop words, and convert to a set of unique terms
        terms = set(normalize(all_text)) - stop_words
        
        # Index each term: map them to their respective movie titles and keep track of term frequency
        for term in terms:
            index['all'][term].add(title)
            term_frequency['all'][term][title] += 1
    
    # Return the constructed indices and the set of person names
    return index, term_frequency, person_name_set

# Implement the refined search function
def search(query, index, term_frequency, person_name_set):
    # Normalize the query to ensure case insensitivity
    query = query.lower()

    # Split the query into the field and search term, assuming a format "field:term"
    # Default to searching all fields if ':' is not present
    field, search_term = query.split(':') if ':' in query else ('all', query)
    
    # Initialize a set to store unique search results
    results = set()

    # Validate the presence of the field in the index
    if field not in index:
        print(f"Invalid field '{field}' in query. Available fields are: title, year, rating, genre, certificate, actor, director.")
        return []

    # Handle range queries for years and ratings
    if field == 'year' and '-' in search_term:
        start, end = map(int, search_term.split('-'))
        for year in range(start, end + 1):
            results.update(index['year'].get(str(year), set()))
    elif field == 'rating' and '-' in search_term:
        start, end = map(float, search_term.split('-'))
        for rating in index['rating']:
            if start <= float(rating) <= end:
                results.update(index['rating'][rating])

    # Handle searches for specific fields using fuzzy matching
    else:
        # Enhanced handling for actor and director fields to accommodate partial names
        if field in ['actor', 'director']:
            # Use partial_ratio to better match partial names
            matches = process.extract(search_term, index[field].keys(), scorer=fuzz.partial_ratio, limit=10)
            # Adjust threshold based on testing or requirements, here set to 75 for demonstration
            for match, score in matches:
                if score > 75:
                    results.update(index[field][match])
        # Standard fuzzy matching for other fields
        else:
            matches = process.extract(search_term, index[field].keys(), limit=5)
            for match, score in matches:
                if score > 80:
                    results.update(index[field][match])

    # Sort the results by relevance using term frequencies of the terms in each movie
    ranked_results = sorted(results, 
                            key=lambda movie: sum(term_frequency['all'][term][movie] for term in normalize(movie)),
                            reverse=True)
    
    return ranked_results

# Command-line interface function
def cli(index, term_frequency, person_name_set):
    # Map numeric options to index fields
    field_map = {
        1: 'title',
        2: 'year',
        3: 'rating',
        4: 'genre',
        5: 'certificate',
        6: 'actor',
        7: 'director'
    }

    # Helper function to display instructions
    def print_help():
        print("\nIMDB Top 250 Movies Search Application Instructions:")
        print("Select a field by number and provide your search term. For example, '2: 1994' to search by year.")
        print("1: Title\n2: Year\n3: Rating\n4: Genre\n5: Certificate\n6: Actor\n7: Director")
        print("For year and rating, you can use ranges like '2: 1990-2000' or '3: 8.5-9.0'")
        print("\nExample queries:")
        print("  - 1: Shawshank Redemption")
        print("  - 2: 1994")
        print("  - 3: 9.3")
        print("  - 4: Drama")
        print("  - 5: R")
        print("  - 6: Leonardo DiCaprio")
        print("  - 7: Christopher Nolan")

    # Welcome message and initial help instructions
    print("Welcome to the IMDB Top 250 Movies Search Application!")
    print_help()

    # Main loop to handle user input
    while True:
        query = input("\nEnter your search query (or 'exit' to quit, 'help' for instructions): ").strip()
        if query.lower() == 'exit':
            break
        if query.lower() == 'help':
            print_help()
            continue

        # Validate the input format
        if ':' not in query:
            print("Error: You must specify a field. Please enter a query in the format 'field number: search term'.")
            continue

        num, search_term = query.split(':', 1)
        num = num.strip()
        search_term = search_term.strip()

        # Validate the field number
        if not num.isdigit() or int(num) not in field_map:
            print("Error: Invalid field number. Please enter a valid number (1-7).")
            continue

        # Ensure the search term is not empty
        if not search_term:
            print("Error: Search term cannot be empty.")
            continue

        # Map the numeric input to the corresponding field
        field = field_map[int(num)]

        # Sanitize the input to remove unwanted characters
        search_term = re.sub(r'[^\w\s\-\.]', '', search_term)

        # Special handling for range queries on year and rating
        if field in ['year', 'rating'] and '-' in search_term:
            try:
                start, end = map(float, search_term.split('-'))
                if start > end:
                    print(f"Error: Invalid {field} range. Start value should be less than or equal to end value.")
                    continue
                if field == 'year' and (start < 1800 or end > 2100):
                    print("Error: Year should be between 1800 and 2100.")
                    continue
                if field == 'rating' and (start < 0 or end > 10):
                    print("Error: Rating should be between 0 and 10.")
                    continue
            except ValueError:
                print(f"Error: Invalid {field} range format. Use format 'start-end'.")
                continue

        # Construct the query for searching
        query = f"{field}: {search_term}"
        
        # Execute the search and handle any exceptions
        try:
            results = search(query, index, term_frequency, person_name_set)
        except Exception as e:
            print(f"An error occurred while searching: {e}")
            continue
        
        # Display search results or provide feedback on no results
        if results:
            print(f"\nFound {len(results)} movies matching query '{query}':")
            while True:
                display_count = input("How many results would you like to see? (Enter a number or 'all'): ")
                if display_count.lower() == 'all':
                    for movie in results:
                        print(f" - {movie}")
                    break
                elif display_count.isdigit() and int(display_count) > 0:
                    for movie in results[:int(display_count)]:
                        print(f" - {movie}")
                    break
                else:
                    print("Invalid input. Please enter a positive number or 'all'.")
        else:
            print(f"No movies found matching your query '{query}'.")
            if field == 'year':
                print("Tip: Make sure the year is within the range of movies in our database (typically 1920-2023).")
            elif field == 'rating':
                print("Tip: Ratings are typically between 7.0 and 9.5 for top movies.")
            elif field in ['actor', 'director']:
                print("Tip: Check the spelling of the name or try a partial name.")

# Main function
def main():
    file_path = 'data/IMDB Top 250 Movies.csv'
    try:
        movies = read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: CSV file '{file_path}' not found.")
        return
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return
    
    inverted_index, term_frequency, person_name_set = build_inverted_index(movies)
    cli(inverted_index, term_frequency, person_name_set)

# Run the main function
if __name__ == "__main__":
    main()