import requests
from bs4 import BeautifulSoup
import streamlit as st

def scrape_wikipedia_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    content = soup.find(id='mw-content-text')
    sections = content.find_all('h2')  # Find all section headings

    berlin_section = None
    for section in sections:
        if section.text.strip() == "Berlin":  # Find the section with the heading "Berlin"
            berlin_section = section
            break

    if berlin_section:
        postal_codes = []
        sibling = berlin_section.next_sibling  # Get the next sibling of the Berlin section
        while sibling and sibling.name != 'h2':
            if sibling.name == 'ul':  # Extract postal codes from unordered list
                items = sibling.find_all('li')
                for item in items:
                    postal_codes.append(item.text.strip())
            sibling = sibling.next_sibling

        return postal_codes
    else:
        return None

def main():
    st.set_page_config(page_icon="💰")
    st.title("Wikipedia Web Scraper 💰")
    url = "https://simple.wikipedia.org/wiki/Postal_codes_in_Germany#Berlin"

    if st.button("Scrape"):
        postal_codes = scrape_wikipedia_page(url)
        if postal_codes:
            st.header("Postal Codes in Berlin:")
            for code in postal_codes:
                st.write(code)
        else:
            st.write("Berlin section not found")

if __name__ == '__main__':
    main()
