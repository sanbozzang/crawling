from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import random
import re
import ssl
import json


def getLink(wikiurl, context):
    links = {}
    html = urlopen(wikiurl, context=context)
    bsObj = BeautifulSoup(html, "html.parser")
    p = re.compile(r":(?!가공)(.+?)(를|을)")
    if bsObj.find("div", {"id": "mw-subcategories"}):
        for link in bsObj.find("div", {"id": "mw-subcategories"}).findAll("a"):
            if 'href' in link.attrs:
                if p.search(link.attrs["title"]):
                    country = p.search(link.attrs["title"]).group(1)
                    links[country] = link.attrs["href"]

    return links


def getTitle(wikiurl, context):
    titles = []
    html = urlopen(wikiurl, context=context)
    bsObj = BeautifulSoup(html, "html.parser")
    if bsObj.find("div", {"id": "mw-pages"}):
        for link in bsObj.find("div", {"id": "mw-pages"}).findAll("a"):
            title = link.attrs["title"]
            titles.append(title)
    return titles


def main():
    context = ssl._create_unverified_context()
    # 1. country를 key로 하는 각 위키 백과 링크 얻기
    countryLinks = getLink(
        "https://ko.wikipedia.org/wiki/%EB%B6%84%EB%A5%98:%EB%82%98%EB%9D%BC%EB%B3%84_%EB%B0%B0%EA%B2%BD%EC%9C%BC%EB%A1%9C_%ED%95%9C_%EC%98%81%ED%99%94", context)

    # print(countryLinks)

    # 2.
    # 1) coutry -> city 링크 존재 시, city 별로 영화 얻기
    # 2) city 링크 없으면 country 별로 영화 얻기
    cityMovies = {}
    countryMovies = {}

    if countryLinks:
        for country in countryLinks:
            cityLinks = getLink(
                "https://ko.wikipedia.org"+countryLinks[country], context)
            if cityLinks:
                for city in cityLinks:
                    cityMovies[city] = getTitle(
                        "https://ko.wikipedia.org"+cityLinks[city], context)
                countryMovies[country] = cityMovies
                cityMovies = {}
            else:
                countryMovies[country] = getTitle(
                    "https://ko.wikipedia.org"+countryLinks[country], context)

    # print(countryMovies)

    # json 변환 후 파일 저장
    countryMoviesJson = json.dumps(countryMovies, ensure_ascii=False)
    f = open("movieData.json", 'w')
    f.write(countryMoviesJson)
    # print(countryMoviesJson)
    print(type(countryMoviesJson))

    # 각 영화 별로 데이터 얻기 -> 기본정보 및 네이버 영화 평점 및 리뷰까지 끌고 오기


if __name__ == '__main__':
    main()
