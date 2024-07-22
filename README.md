# IMDB Top 250 Movies Search Application

## Project Overview
The IMDB Top 250 Movies Search Application is a command-line interface (CLI) based application that allows users to search for movies from the IMDB Top 250 list based on various criteria such as title, year, genre, actors, and directors. The application employs a simple yet robust search functionality incorporating fuzzy matching to enhance user experience by handling approximate searches effectively.

## Features
- **Search by Title**: Look up movies by entering partial or full movie titles.
- **Search by Year**: Retrieve movies from specific years or within a range of years.
- **Search by Rating**: Find movies based on their IMDB rating.
- **Search by Genre**: Filter movies by genre (e.g., Drama, Comedy).
- **Search by Cast and Directors**: Search for movies by actor or director names using fuzzy matching to account for partial inputs or minor misspellings.
- **Range Queries**: Supports range queries for years and ratings to fetch movies within certain intervals.

## Technologies Used
- **Python**: The primary programming language used.
- **fuzzywuzzy**: Python library for fuzzy string matching.
- **nltk**: Natural language toolkit for Python used for text processing.

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Git (optional, recommended for cloning the repository)

### Installation
1. **Clone the Repository** (if Git is installed): git clone https://github.com/yourusername/imdb-search-app.git
2. **Change Directory** : cd imdb-search-app
3. **Alternatively, download the ZIP file of the project and extract it.**
4. **Set Up a Python Virtual Environment** (optional, but recommended): python -m venv venv. source venv/bin/activate # On Windows use venv\Scripts\activate
5. **Install Required Packages**: pip install -r requirements.txt

## How to Use
Run the application using: python search_app.py

### Example Queries
- **Search by Title**: 1: Shawshank Redemption
- **Search by Year**: 2: 1994
- **Search by Actor**: 6: Morgan Freeman

## Extensibility
- **Web Interface**: Future iterations could include a web-based interface for easier access and interaction.
- **Real-time Data**: Integration with real-time databases to include more than the top 250 movies and update the list dynamically.
- **Advanced Search Features**: Implementing advanced search filters and sorting options to enhance user searches.
- **User Authentication and Profiles**: Adding user management to save favorite movies and search history.

## Contributing
Contributions are welcome! Please read `CONTRIBUTING.md` for details on our code of conduct and the process for submitting pull requests to us.

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details.

## Contact
For any queries, you can reach out to [Archit Gupta](mailto:archit@ucsb.edu).

Thank you for checking out the IMDB Top 250 Movies Search Application!






