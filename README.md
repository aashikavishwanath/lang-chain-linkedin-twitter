## PersonaInsight Project Overview

PersonaInsight is an intelligent profile summarizer that scrapes and analyzes LinkedIn and Twitter profiles.  By simply entering a person's name, the platform searches for the LinkedIn profile URL, scrapes information from the profile, retrieves recent tweets, and constructs a summary. The information includes a short summary, interesting facts, topics of interest, and creative ice breakers to open a conversation with the person. The project consists of both a backend that handles data scraping and summarizing and a frontend that provides an interactive user interface.

## Features

1. **LinkedIn Profile Scraper**: Fetches and scrapes LinkedIn profile information.
2. **Twitter Profile Scraper**: Retrieves recent tweets from a given Twitter handle.
3. **Profile Summary Generator**: Constructs a summary based on the scraped LinkedIn and Twitter data.
4. **Search Engine Integration**: Utilizes custom search engine integration to look up LinkedIn profiles.
5. **Interactive Frontend:** A user-friendly interface for inputting names and viewing summaries.
6. **Loading Spinner:** A visually appealing loading spinner that provides feedback while the backend processes the request.

## Technologies Used

### Backend

1. **Requests**: For making HTTP requests to scrape data.
2. **OpenAI**: Utilized for generating summaries and constructing ice breakers.
3. **SerpAPI**: Custom integration with SerpAPI to fetch LinkedIn profiles through search engines.
4. **RapidAPI**: Used for interacting with Twitter's API.
5. **Langchain**: A library for chaining different language models to perform complex tasks.
6. **Pydantic**: For data parsing and validation.
7. **Environment Variables**: For secure handling of API keys.

### Frontend

1. **HTML/CSS**: Basic structure and styling of the web page.
2. **jQuery**: Handling form submission and AJAX calls to the backend.
3. **FontAwesome**: For loading spinner and other iconography.

## How to Use

### Requirements

- Python 3.x
- An API key for OpenAI, SerpAPI, and RapidAPI
- An authorization token for scraping LinkedIn via ProxyCurl
- A web server like Flask to serve the HTML page and handle AJAX requests

### Installation

1. Clone the repository.
2. Install the required dependencies:

```bash
pip install requests openai langchain pydantic
```

3. Set the required environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key
- `PROXYCURL_API_KEY`: Your ProxyCurl API key for LinkedIn scraping
- `X-RAPIDAPI-KEY`: Your RapidAPI key for Twitter scraping
- `X-RAPIDAPI-HOST`: Your RapidAPI host for Twitter scraping
- `SERP_API_KEY`: Your SerpAPI key for LinkedIn profile search

4. Run the script:

```bash
python your_script_name.py
```

Replace `your_script_name.py` with the name of the script.

5. Place the HTML file in the appropriate directory of your web server.
6. Link the CSS file in your HTML's `<head>` section.
7. Configure the server-side endpoint (`/process`) to handle the AJAX request from the frontend and return the required JSON data.
   
## Functionality

1. **`scrape_linkedin_profile(linkedin_profile_url: str)`**: Scraps LinkedIn profile information.
2. **`scrape_twitter_profile(twitter_string: str)`**: Scraps Twitter profile information.
3. **`get_profile_url(name: str)`**: Searches for the LinkedIn profile URL.
4. **`lookup(name: str) -> str`**: Retrieves the LinkedIn profile URL using Langchain's agent.
5. **`do_task(name: str)`**: Main function to perform the task of scraping and summarizing the profile.

## Conclusion

PersonaInsight elegantly weaves frontend and backend technologies to provide an intuitive and informative experience. By combining web scraping, AI-powered summarization, natural language processing, and a user-friendly interface, it offers valuable insights into individuals' digital personas. It can be further extended to support more social platforms or to provide more detailed insights.

## Disclaimer

This project is for educational purposes only. Please make sure to comply with LinkedIn, Twitter, and other relevant terms of service, especially regarding the scraping of data.
