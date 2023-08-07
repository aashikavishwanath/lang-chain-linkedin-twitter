## PersonaInsight Project Overview

This project is designed to scrape and analyze both LinkedIn and Twitter profiles. Given a full name, it searches for the LinkedIn profile URL, scrapes information from the profile, retrieves recent tweets, and constructs a summary. The information includes a short summary, interesting facts, topics of interest, and creative ice breakers to open a conversation with the person.

## Features

1. **LinkedIn Profile Scraper**: Fetches and scrapes LinkedIn profile information.
2. **Twitter Profile Scraper**: Retrieves recent tweets from a given Twitter handle.
3. **Profile Summary Generator**: Constructs a summary based on the scraped LinkedIn and Twitter data.
4. **Search Engine Integration**: Utilizes custom search engine integration to look up LinkedIn profiles.

## Technologies Used

1. **Requests**: For making HTTP requests to scrape data.
2. **OpenAI**: Utilized for generating summaries and constructing ice breakers.
3. **SerpAPI**: Custom integration with SerpAPI to fetch LinkedIn profiles through search engines.
4. **RapidAPI**: Used for interacting with Twitter's API.
5. **Langchain**: A library for chaining different language models to perform complex tasks.
6. **Pydantic**: For data parsing and validation.
7. **Environment Variables**: For secure handling of API keys.

## How to Use

### Requirements

- Python 3.x
- An API key for OpenAI, SerpAPI, and RapidAPI
- An authorization token for scraping LinkedIn via ProxyCurl

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

## Functionality

1. **`scrape_linkedin_profile(linkedin_profile_url: str)`**: Scraps LinkedIn profile information.
2. **`scrape_twitter_profile(twitter_string: str)`**: Scraps Twitter profile information.
3. **`get_profile_url(name: str)`**: Searches for the LinkedIn profile URL.
4. **`lookup(name: str) -> str`**: Retrieves the LinkedIn profile URL using Langchain's agent.
5. **`do_task(name: str)`**: Main function to perform the task of scraping and summarizing the profile.

## Conclusion

This project demonstrates an interesting use case of combining various web scraping techniques with natural language processing to create a comprehensive profile summary. It can be further extended to support more social platforms or to provide more detailed insights.

## Disclaimer

This project is for educational purposes only. Please make sure to comply with LinkedIn, Twitter, and other relevant terms of service, especially regarding the scraping of data.
