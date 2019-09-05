import pandas as pd
from bs4 import BeautifulSoup
import os
import time
import codecs

def get_articles():
	articles = os.listdir("pages")
	return articles

def get_headline(article):
	path = "pages/" + article
	with codecs.open(path, "r", "utf-8") as file:
		for line in file:
			if "headline" in line:
				line = line.replace("\t", "").replace('"headline":', "").replace(" ", "", 5)
				line = line.replace("\n", "").replace(",", "").replace('"', "", 1).replace('"', "", -1)
				line = line.replace("Ä", "Ae").replace("ä", "ae").replace("Ö", "Oe").replace("ö", "oe")
				line = line.replace("Ü", "Ue").replace("ü", "ue").replace("ß", "ss").replace("\\", "")
				line = line.replace(" ", " ")
				return line

def get_type(article):
	path = "pages/" + article
	with codecs.open(path, "r", "utf-8") as file:
		for line in file:
			if "@type" in line:
				line = line.replace("\t", "").replace('"@type":', "").replace(" ", "", 5)
				line = line.replace("\n", "").replace(",", "").replace('"', "", 1).replace('"', "", -1)
				line = line.replace("Ä", "Ae").replace("ä", "ae").replace("Ö", "Oe").replace("ö", "oe")
				line = line.replace("Ü", "Ue").replace("ü", "ue").replace("ß", "ss").replace("\\", "")
				line = line.replace(" ", " ")
				return line

def get_url(article):
	path = "pages/" + article
	with codecs.open(path, "r", "utf-8") as file:
		for line in file:
			if '"url":' in line:
				line = line.replace("\t", "").replace('"url":', "").replace(" ", "", 5)
				line = line.replace("\n", "").replace(",", "").replace('"', "", 1).replace('"', "", -1)
				line = line.replace("Ä", "Ae").replace("ä", "ae").replace("Ö", "Oe").replace("ö", "oe")
				line = line.replace("Ü", "Ue").replace("ü", "ue").replace("ß", "ss").replace("\\", "")
				line = line.replace(" ", " ")
				return line

def get_creators(article):
	path = "pages/" + article
	with codecs.open(path, "r", "utf-8") as file:
		for line in file:
			if '"creator":' in line:
				line = line.replace("\t", "").replace('"creator":', "").replace(",", ":")
				line = line.replace("\n", "").replace('"', "", 1).replace('"', "", -1)
				line = line.replace("Ä", "Ae").replace("ä", "ae").replace("Ö", "Oe").replace("ö", "oe")
				line = line.replace("Ü", "Ue").replace("ü", "ue").replace("ß", "ss").replace("\\", "")
				line = line.replace(" ", " ").replace("[", "").replace("]", "")
				line = line[::-1]
				line = line.replace(":", "", 1)
				line = line[::-1]
				authors = line.split(":")
				return authors

def get_keywords(article):
	path = "pages/" + article
	with codecs.open(path, "r", "utf-8") as file:
		for line in file:
			if '"keywords":' in line:
				line = line.replace("\t", "").replace('"keywords":', "").replace(",", "thisIsASplitter")
				line = line.replace("\n", "").replace('"', "")
				line = line.replace("Ä", "Ae").replace("ä", "ae").replace("Ö", "Oe").replace("ö", "oe")
				line = line.replace("Ü", "Ue").replace("ü", "ue").replace("ß", "ss").replace("\\", "")
				line = line.replace(" ", " ").replace("[", "").replace("]", "")
				keywords = line.split("thisIsASplitter")
				return keywords

def get_date(article):
	path = "pages/" + article
	with codecs.open(path, "r", "utf-8") as file:
		for line in file:
			if '"datePublished":' in line:
				line = line.replace("\t", "").replace("\n", "").replace('"datePublished": ', "")
				line = line.replace('"', "")
				line = line[:10]
				return line

def get_time(article):
	path = "pages/" + article
	with codecs.open(path, "r", "utf-8") as file:
		for line in file:
			if '"datePublished":' in line:
				line = line.replace("\t", "").replace("\n", "").replace('"datePublished": ', "")
				line = line.replace('"', "")
				line = line[11:19]
				return line

articles = get_articles()
table = pd.DataFrame(columns = ["article", "headline", "type", "authors", "keywords", "date", "time", "url"])
for article in articles:
	headline = get_headline(article)
	type_ = get_type(article)
	url = get_url(article)
	authors = get_creators(article)
	keywords = get_keywords(article)
	date = get_date(article)
	time = get_time(article)
	df = pd.DataFrame([[article, headline, type_, authors, keywords, date, time, url]],
		columns = ["article", "headline", "type", "authors", "keywords", "date", "time", "url"])
	table = table.append(df, ignore_index = True)

table.to_csv("good_table.csv", index = False)
	
	