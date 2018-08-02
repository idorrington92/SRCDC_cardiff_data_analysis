
# This code amalgamates the summary information from the 'mylocalschool.wales' website into one large dictionary for easy access. 
import requests
from bs4 import BeautifulSoup

def make_school_URL_dict_from_list(schools):
    toppage = requests.get("http://mylocalschool.wales.gov.uk/Schools/SchoolSearch?lang=en")
    soup = BeautifulSoup(toppage.content, 'html.parser')
    school_links = soup.select("a[href*=/School]")[2:]
    schools = [list(school.children)[0] for school in school_links]
    school_URLs = ["http://mylocalschool.wales.gov.uk" + school['href'] for school in school_links]
    schoolURL_dict = {}
    for s,school in enumerate(schools):
        schoolURL_dict[school] = school_URLs[s]
    return schoolURL_dict


def tofloat(string):
    try:
        output = float(string)
    except ValueError:
        output = string
    return output
                
def make_stat_dict(schoolURL):
    school_pages = requests.get(schoolURL)
    school_soup = BeautifulSoup(school_pages.content, 'html.parser')
    summary = school_soup.find_all('div',id=False, class_="summaryBox")
    stat_dict = {}
    for i in range(len(summary)):
        stat = ''.join(char for char in list(summary[i].children)[1].getText() if char.isalnum() or char=='.')
        stat = tofloat(stat)
        stat_name = (''.join(char for char in list(summary[i].children)[3].getText() if char.isalnum() or char==' ')).strip()
        if '%' in list(summary[i].children)[1].getText(): stat_name += "(%)"
        stat_dict[stat_name] = stat
    return stat_dict

def make_district_school_URLdict(district): 
    toppage = requests.get("http://mylocalschool.wales.gov.uk/Schools/SchoolSearch?lang=en")
    soup = BeautifulSoup(toppage.content, 'html.parser')
    url_ref = [list(soup.find_all("option"))[-1]['value'] for i in range(len(list(soup.select('option'))))                                             if list(soup.find_all("option")[i])[0].strip() == district][0]
    school_url_string = "a[href*=/School/" + url_ref + "]"
    school_links = soup.select(school_url_string)
    schools = [list(school.children)[0] for school in school_links]
    school_URLs = ["http://mylocalschool.wales.gov.uk" + school['href'] for school in school_links]
    schoolURL_dict = {}
    for s,school in enumerate(schools):
        schoolURL_dict[school] = school_URLs[s]
    return schoolURL_dict


def make_district_school_URLdict_by_type(district,schools=False):
    school_URLs = make_district_school_URLdict(district)
    schools_URLdict = {}
    for school in school_URLs.keys():
        school_pages = requests.get(school_URLs[school])
        school_soup = BeautifulSoup(school_pages.content, 'html.parser')
        school_type = list(school_soup.select("div[class=schDetailsText]")[1].children)[0].strip()
        if 'Primary' in schools:
            if ('Infants' or 'Juniors') in school_type:
                schools_URLdict[school] = school_URLs[school]
        if 'Secondary' in schools:
            if 'Secondary' in school_type:
                schools_URLdict[school] = school_URLs[school]         
    return schools_URLdict

