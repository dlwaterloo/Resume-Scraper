import os
import requests
import re
import logging
from typing import Optional
from linkedin_api import Linkedin, cookie_repository
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain.schema import SystemMessage

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables
LINKEDIN_USERNAME = os.environ.get("LINKEDIN_USERNAME")
LINKEDIN_PASSWORD = os.environ.get("LINKEDIN_PASSWORD")
PROXYCURL_API_KEY = os.environ.get("PROXYCURL_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# LinkedIn client setup
def linkedin_client():
    cookies_dir = "./misc/"
    cookies_repo = cookie_repository.CookieRepository(cookies_dir)
    return Linkedin(username=LINKEDIN_USERNAME, password=LINKEDIN_PASSWORD, cookies=cookies_repo.get(LINKEDIN_USERNAME))

# Utility function to remove text inside parentheses
def remove_inside_parentheses(s: str) -> str:
    return re.sub(r"\([^)]*\)", "", s).strip()

# Search for LinkedIn profiles
def linkedin_resume_search(job_title: str, company_name: str, max_results: int) -> list:
    try:
        client = linkedin_client()
        search_keywords = f"{remove_inside_parentheses(job_title)} resume"
        search_results = client.search_people(
            keywords=search_keywords,
            keyword_company=remove_inside_parentheses(company_name),
            include_private_profiles=True,
            limit=max_results
        )

        return [result["urn_id"] for result in search_results] if search_results else []
    except Exception as e:
        logger.error(f"LinkedIn resume search error: {e}")
        return []


# Retrieve LinkedIn profile details
def get_linkedin_profile(urn_id: str):
    linkedin_profile_url = f"https://www.linkedin.com/in/{urn_id}"
    api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
    headers = {'Authorization': f'Bearer {PROXYCURL_API_KEY}'}

    try:
        response = requests.get(api_endpoint, params={'url': linkedin_profile_url, 'skills': 'include'}, headers=headers)
        if response.ok:
            profile_data = response.json()
            summary = profile_data.get('summary', '')  or ''
            featured = profile_data.get('featured', '')
            print("featured", featured)
            first_name = profile_data.get('first_name', '')
            last_name = profile_data.get('last_name', '')

            # Check for URL-like patterns in the summary
            if re.search(r'https?://[^\s]+', summary):
                return {"summary": summary, "first_name": first_name, "last_name": last_name, "potential_link": True}
            else:
                return {"summary": summary, "first_name": first_name, "last_name": last_name, "potential_link": False}
        else:
            print("Unsuccessful response")
            return None
    except Exception as e:
        print("get_linkedin_profile error: ", e)
        return None

# LangChain function to extract resume link
def GPT4():
    return ChatOpenAI(model="gpt-4", temperature=0.4)

def extract_resume_link_with_langchain(about_text: str) -> Optional[str]:
    llm = GPT4()

    system_message = SystemMessage(
        content="You are a smart assistant. Extract any links if presented in this text."
    )

    human_message_template = HumanMessagePromptTemplate.from_template("{about_text}")

    prompt_template = ChatPromptTemplate.from_messages([system_message, human_message_template])

    prompt = prompt_template.format_messages(about_text=about_text)

    try:
        response = llm.invoke(prompt)
        if response is None or not hasattr(response, 'content'):
            raise ValueError("No content in the response")

        response_content = response.content
        if not response_content:
            raise ValueError("Empty response content")

        # Use regex to extract the URL from the response
        url_match = re.search(r'(https?://[^\s]+)', response_content)
        return url_match.group(0) if url_match else None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
