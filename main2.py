from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
import requests
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List
import openai
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
import os


openai_api_key = os.environ.get("OPENAI_API_KEY")
print('openai_api_key', openai_api_key)

def scrape_linkedin_profile(linkedin_profile_url: str):
    """scrape information from LinkedIn profiles,
    Manually scrape the information from the LinkedIn profile"""
    api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
    api_key = os.environ.get("PROXYCURL_API_KEY")
    header_dic = {'Authorization': 'Bearer ' + api_key}
    params = {
        'url': linkedin_profile_url,
    }
    response = requests.get(api_endpoint,
                            params=params,
                            headers=header_dic)
    print('response.text:', response.text)
    data = response.json()
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None)
        and k not in ["people_also_viewed", "certifications"]
    }
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")

    return data

def scrape_twitter_profile(twitter_string: str):
    """scrape information from LinkedIn profiles,
    Manually scrape the information from the LinkedIn profile"""

    url = "https://twitter135.p.rapidapi.com/AutoComplete/"

    querystring = {"q":twitter_string}

    headers = {
      "X-RapidAPI-Key": os.environ.get("X-RAPIDAPI-KEY"),
      "X-RapidAPI-Host": os.environ.get("X-RAPIDAPI-HOST")
    }

    response = requests.get(url, headers=headers, params=querystring)

    id_string = response.json()['users'][0]['id_str']

    url2 = "https://twitter135.p.rapidapi.com/v2/UserTweets/"

    querystring2 = {"id":id_string,"count":"5"}

    headers2 = {
      "X-RapidAPI-Key": os.environ.get("X-RAPIDAPI-KEY"),
      "X-RapidAPI-Host": os.environ.get("X-RAPIDAPI-HOST")
    }

    response2 = requests.get(url2, headers=headers2, params=querystring2)

    data = response2.json()

    tweets_dict = {}

    for i in range(10):
        tweet_key = f"tweet{i+1}"
        try:
            tweet_data = data['data']['user']['result']['timeline_v2']['timeline']['instructions'][1]['entries'][i]['content']['itemContent']['tweet_results']['result']['legacy']['full_text']
        except (KeyError, IndexError):
            break
        if "RT @" not in tweet_data and not tweet_data.startswith('@'):
            tweets_dict[tweet_key] = tweet_data

    return tweets_dict


from langchain.utilities import SerpAPIWrapper


class CustomSerpAPIWrapper(SerpAPIWrapper):
    def __init__(self, api_key: str):
        super(CustomSerpAPIWrapper, self).__init__(serpapi_api_key=api_key)

    @staticmethod
    def _process_response(res: dict) -> str:
        """Process response from SerpAPI."""
        if "error" in res.keys():
            raise ValueError(f"Got error from SerpAPI: {res['error']}")
        if "answer_box" in res.keys() and "answer" in res["answer_box"].keys():
            toret = res["answer_box"]["answer"]
        elif "answer_box" in res.keys() and "snippet" in res["answer_box"].keys():
            toret = res["answer_box"]["snippet"]
        elif (
            "answer_box" in res.keys()
            and "snippet_highlighted_words" in res["answer_box"].keys()
        ):
            toret = res["answer_box"]["snippet_highlighted_words"][0]
        elif (
            "sports_results" in res.keys()
            and "game_spotlight" in res["sports_results"].keys()
        ):
            toret = res["sports_results"]["game_spotlight"]
        elif (
            "knowledge_graph" in res.keys()
            and "description" in res["knowledge_graph"].keys()
        ):
            toret = res["knowledge_graph"]["description"]
        elif "snippet" in res["organic_results"][0].keys():
            toret = res["organic_results"][0]["link"]

        else:
            toret = "No good search result found"
        return toret


def get_profile_url(name: str):
    """Searches for Linkedin or twitter Profile Page."""
    key = os.environ.get("SERP_API_KEY")
    search = CustomSerpAPIWrapper(api_key=key)
    res = search.run(f"{name}")
    return res


def lookup(name: str) -> str:
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", openai_api_key=openai_api_key)

    template = """given the full name {name_of_person} I want you to get it me a link to their Linkedin profile page.
                          Your answer should contain only a URL"""
    tools_for_agent1 = [
        Tool(
            name="Crawl Google 4 linkedin profile page",
            func=get_profile_url,
            description="useful for when you need get the Linkedin Page URL",
        ),
    ]

    agent = initialize_agent(
        tools_for_agent1, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
    )
    prompt_template = PromptTemplate(
        input_variables=["name_of_person"], template=template
    )
    linkedin_username = agent.run(prompt_template.format_prompt(name_of_person=name))

    return linkedin_username


class PersonIntel(BaseModel):
    summary: str = Field(description="Summary of the person")
    facts: List[str] = Field(description="Interesting facts about the person")
    topics_of_interest: List[str] = Field(description="Topics that may interest the person")
    ice_breakers: List[str] = Field(description="Creation ice breakers to open a conversation with the person")

    def to_dict(self):
        return {"summary": self.summary, "facts": self.facts, "topics_of_interest": self.topics_of_interest,
                "ice_breakers": self.ice_breakers}


person_intel_parser = PydanticOutputParser(pydantic_object=PersonIntel)


def do_task(name: str):
    linkedin_profile_url = lookup(name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_profile_url)

    tweets = scrape_twitter_profile(name)
    summary_template = """
        given the linkedin information {linkedin_information} and twitter {twitter_information} about a person from I want you to create:
        1. a short summary
        2. two interesting facts about them
        3. a topic that may interest them
        4. 2 creative ice breakers to open a conversation with them
                \n{format_instructions}
    """

    summary_prompt_template = PromptTemplate(input_variables=["linkedin_information", "twitter_information"],
                                             template=summary_template, partial_variables={
            "format_instructions": person_intel_parser.get_format_instructions()})

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", openai_api_key=openai_api_key)

    chain = LLMChain(llm=llm, prompt=summary_prompt_template)

    result = chain.run(linkedin_information=linkedin_data, twitter_information=tweets)

    return person_intel_parser.parse(result), linkedin_data.get("profile_pic_url")


if __name__ == '__main__':

    do_task("harrison chase")

