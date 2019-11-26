import os
from bs4 import BeautifulSoup
import requests
import argparse
import sys

def login(url, session, headers = {}, log_info = {}):
    """Log into url using POST.

    Logs into a site on the web given by url, using provided login information
    and headers through POST method. The session is maintained.
    """
    try:
        response = session.post(url, data=log_info, headers = headers)
    except requests.RequestException as rex:
        print(str(rex))
    else:
        return response
    
def clean(dirty, delimeter="\n"):
    """Clean provided string and enter into dict.

    Cleans unparsed information based first on delimeter (default newline),
    then on colon. Fills a dict with the cleaned information
    """
    clean_info = {}
    split_dirty = dirty.split(delimeter)
    for line in split_dirty:
        key_value = line.split(":", 1)
        clean_info[key_value[0]] = key_value[1]
    return clean_info

def get_file_text(file_name):
    """Get text from file."""
    with open(file_name, "r") as f:
        text=f.read()
    return text

def main(url, header_file="headersinfo.txt", login_file="loginfo.txt"):
    headers = {}
    headers = clean(get_file_text(header_file), "\n")
    log_info = {}
    log_info = clean(get_file_text(login_file), "\n")
    with requests.Session() as session:
        login(
            "https://www.rep-am.com/login", session, headers = headers, log_info = log_info)
        try:
            info = session.get(url)
        except requests.RequestException as rex:
            print(str(rex))
        else:
            soup = BeautifulSoup(info.content, "html.parser")
            # with open("debug.txt", "w") as f:
            #     f.write(str(soup))
            incidents = []
            for incident in soup.findAll("p"):
                incidents.append(incident.text)
            with open(new_file:=f"dirty_{url[-4:-1]}.txt", "w") as f:
                f.write(str(incidents))
            return new_file

    
if __name__ == "__main__":    
    # headers = {}
    # headers = clean(get_file_text("headersinfo.txt"), "\n")
    # log_info = {}
    # log_info = clean(get_file_text("loginfo.txt"), "\n")
    try:
        url = sys.argv[1]
    except IndexError:
        url = input("What url to scrape?")
    with requests.Session() as session:
        main(url=url)
        # login(
        #     "https://www.rep-am.com/login", session, headers = headers, log_info = log_info)
        # # url = "https://www.rep-am.com/local/records/police/2019/11/22/torrington-police-blotter-65/"
        # try:
        #     info = session.get(url)
        # except requests.RequestException as rex:
        #     print(str(rex))
        # else:
        #     soup = BeautifulSoup(info.content, "html.parser")
        #     with open("test.txt", "w") as f:
        #         f.write(str(soup))
        #     incidents = []
        #     for incident in soup.findAll("p"):
        #         incidents.append(incident.text)
        #     with open(f"dirty_{url[-4:-1]}.txt", "w") as f:
        #         f.write(str(incidents))