# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
import time
import re


# %%
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# %%
# Import and establish Base for which classes will be constructed
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


# %%
from sqlalchemy import Column, Integer, String, Float


# %%
# Create Article Class
# ----------------------------------
class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    author = Column(String(255))
    link = Column(String)
    subtitle = Column(String)


# %%
class Indicator(Base):
    __tablename__  = 'GHDI'
    id = Column(Integer, primary_key=True)
    country = Column(String(255))
    link = Column(String)


# %%
url = 'https://blogs.worldbank.org/tags/data-news?page=0'
browser.visit(url)


# %%
engine = create_engine("sqlite:///article.sqlite")
conn = engine.connect()


# %%
Base.metadata.create_all(conn)


# %%
from sqlalchemy.orm import Session
session = Session(bind=engine)


# %%
for x in range(1,40):
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    articles = soup.find_all('div', class_="listing")
    articleURL = 'https://blogs.worldbank.org'
    for article in articles:
        print('Page: ' + str(x))
        print('Title: ' + article.find('div', class_='views-field views-field-title').text)
        print('Link: ' + articleURL + article.find('a')['href'])
        print('Author(s): ' + article.find('span', class_='field-content').text)

        articleTitle = article.find('div', class_='views-field views-field-title').text
        articleAuthor = article.find('span', class_='field-content').text
        articleLink = (articleURL + article.find('a')['href'])

        articleSubtitle = 'missing subtitle'

        article = Article(title=articleTitle, author=articleAuthor, link=articleLink, subtitle=articleSubtitle)

        session.add(article)
        session.commit()
    # One bug I found while scraping this website involved the applications failure to move to the next page. It would move between 5-7 pages and then begin repeatedly scraping    the same page. So we added the page change to the loop in order to enforce page changes.
    # browser.click_link_by_partial_text('Next page')
    url = f'https://blogs.worldbank.org/tags/data-news?page={x}'
    browser.visit(url)


# %%
url = 'https://knoema.com/search?query=human%20development&scope=datasets&tab=more'
browser.visit(url)


# %%
html = browser.html
soup = BeautifulSoup(html, 'html.parser')

articles = soup.find_all('div', class_="search-result-item grouped-dataset-content group-show-more")

secondaryArticles = soup.find_all('div', class_="search-result-item ungrouped-dataset")

# For Debugging Purposes
# i = 0

# In this cell we have two seperate for loops being used; this is because the class switches around the halfway mark, from grouped to ungrouped data set. By doing this, we ensure we have found all 99  articles.

def scrape():
    try:
        baseURL = 'https://'
        foundURL = article.find('a')['href']
        fullURL = baseURL + foundURL[2:]
        title = article.find('a').text
        tag = article.find('a', class_="formatted-title external-link").text

        print("fullURL: " + fullURL)
        print("title: " + title)
        print("tag: " + tag)
        # for tag in article.find_all("a", class_="formatted-title external-link"):
        #     print(tag.get_text())
        print("=================================================================")

        articleTitle = title
        articleAuthor = 'missing Author'
        articleLink = fullURL
        articleSubtitle = tag

        newArticle = Article(title=articleTitle, author=articleAuthor, link=articleLink, subtitle=articleSubtitle)

        session.add(newArticle)
        session.commit()
    except (AttributeError, KeyError) as ex:
        pass
    return


for article in articles:
    scrape()

    # For Debugging Purposes
    # i = i + 1
    # print(i)

for article in secondaryArticles:
    scrape()

    # For Debugging Purposes
    # i = i + 1
    # print(i)


# %%
url = 'http://hdr.undp.org/en/countries'
browser.visit(url)


# %%
html = browser.html
soup = BeautifulSoup(html, 'html.parser')

articles = soup.find_all('div', class_="countriesListItem")

for article in articles:
    print('http://hdr.undp.org/en' + article.find('a')['href'])
    print( article.find('a').text)

    country = ('http://hdr.undp.org/en' + article.find('a')['href'])
    link = article.find('a').text

    ghdi = Indicator(country=country, link=link)

    session.add(ghdi)
    session.commit()



# %%


