from luxon.html.parser import Parser
from luxon.html.tags import *
import requests

def main():
    # Just a silly program to scrape the front page of The Hacker News
    # and get the latest article titles and links.
    source = requests.get("https://thehackernews.com/").content.decode("utf-8")
    parsed = Parser.parse(source)

    for blog_post in parsed.find_by_class("blog-posts").find_all_by_class("body-post"):
        story_link = blog_post.find(lambda t: type(t) == A and "story-link" in t.classes)
        home_title = blog_post.find(lambda t: type(t) == H2 and "home-title" in t.classes)
        print((home_title.read_text(), story_link.get('href')))

if __name__ == "__main__":
    main()