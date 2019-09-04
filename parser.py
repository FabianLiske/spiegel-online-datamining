import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import urllib3
import os
import re
import time

if "pages" not in os.listdir():
	os.mkdir("pages")

def getURLList():
	url = "http://www.spiegel.de"
	response = requests.get(url)
	page = str(BeautifulSoup(response.content))
	urls = []

	def getURL(page):
		start_link = page.find("a href")
		if start_link == -1:
			return None, 0
		start_quote = page.find('"', start_link)
		end_quote = page.find('"', start_quote + 1)
		url = page[start_quote + 1: end_quote]
		return url, end_quote

	while True:
		url, n = getURL(page)
		page = page[n:]
		if url:
			if "-a-" in url:
				if "bento" not in url:
					if "matchday" not in url:
						if "forum" not in url:
							url = "http://www.spiegel.de" + url
							urls.append(url)
		else:
			break

	urls = list(dict.fromkeys(urls))

	return urls

def find_new():
	if "urls.csv" in os.listdir():
		prev_urls = pd.read_csv("urls.csv", sep = ",")
	else:
		prev_urls = pd.DataFrame(columns = ["url"])

	prev_urls_list = prev_urls["url"].values.tolist()
	urls_list = getURLList()
	new_urls = []
	for url in urls_list:
		if url not in prev_urls_list:
			new_urls.append(url)
	new_current_urls = prev_urls_list + new_urls
	new_current_urls = pd.DataFrame(new_current_urls, columns = ["url"])
	new_current_urls.to_csv(("urls.csv"), sep = ",", index = False)
	l = len(new_urls)
	if l == 1:
		print("1 new article found.")
		print("Article      HTTP-Response")
	elif l > 1:
		print("{} new articles found.".format(l))
		print("Article      HTTP-Response")
	elif l == 0:
		print("No new articles found.")

	return new_urls

def download_sites():
	urls = find_new()
	dled_pages = os.listdir("pages")
	for url in urls:
		name = url[-12:-5]
		name = name.replace("-", "")
		if name in dled_pages:
			print("{} exists already.".format(name))
		try:
			r = requests.get(url, allow_redirects = True)
			print("{}      {}".format(name, r.status_code))
			open("pages/{}.txt".format(name), "wb").write(r.content)
		except:
			print("Failed")

		time.sleep(5)
	return urls

def get_meta(name):
	def get_type(name):
		string = "@type"
		name = "pages/" + name + ".txt"
		try:
			with open(name, "r") as file:
				for line in file:
					if string in line:
						type_ = line.replace(",", "").replace('"', "").replace(string, "")
						type_ = type_.replace(" ", "").replace(" ", "").replace(":", "")
						type_ = type_.replace("\n", "").replace("\t", "")
						return type_
		except:
			print("Now that didn't work...")

	def get_headline(name):
		string = "headline"
		name = "pages/" + name + ".txt"
		try:
			with open(name, "r") as file:
				for line in file:
					if string in line:
						headline = line.replace(",", "").replace('"', "").replace(string, "")
						headline = headline.replace(" ", "").replace(" ", "").replace(":", "")
						headline = headline.replace("\n", "").replace("\t", "")
						return headline
		except:
			print("Now that didn't work...")

	def get_created(name):
		string = "dateCreated"
		name = "pages/" + name + ".txt"
		try:
			with open(name, "r") as file:
				for line in file:
					if string in line:
						created = line.replace(",", "").replace('"', "").replace(string, "")
						created = created.replace(" ", "").replace(" ", "").replace(":", "")
						created = created.replace("\n", "").replace("\t", "")
						return created
		except:
			print("Now that didn't work...")

	def get_published(name):
		string = "datePublished"
		name = "pages/" + name + ".txt"
		try:
			with open(name, "r") as file:
				for line in file:
					if string in line:
						published = line.replace(",", "").replace('"', "").replace(string, "")
						published = published.replace(" ", "").replace(" ", "").replace(":", "")
						published = published.replace("\n", "").replace("\t", "")
						return published
		except:
			print("Now that didn't work...")

	def get_modified(name):
		string = "dateModified"
		name = "pages/" + name + ".txt"
		try:
			with open(name, "r") as file:
				for line in file:
					if string in line:
						modified = line.replace(",", "").replace('"', "").replace(string, "")
						modified = modified.replace(" ", "").replace(" ", "").replace(":", "")
						modified = modified.replace("\n", "").replace("\t", "")
						return modified
		except:
			print("Now that didn't work...")

	def get_section(name):
		string = "articleSection"
		name = "pages/" + name + ".txt"
		try:
			with open(name, "r") as file:
				for line in file:
					if string in line:
						section = line.replace(",", "").replace('"', "").replace(string, "")
						section = section.replace(" ", "").replace(" ", "").replace(":", "")
						section = section.replace("\n", "").replace("\t", "")
						return section
		except:
			print("Now that didn't work...")

	def get_creator(name):
		string = "creator"
		name = "pages/" + name + ".txt"
		try:
			with open(name, "r") as file:
				for line in file:
					if string in line:
						creator = line.replace(",", "").replace('"', "").replace(string, "").replace("[", "")
						creator = creator.replace(" ", "").replace(" ", "").replace(":", "").replace("]", "")
						creator = creator.replace("\n", "").replace("\t", "")
						return creator
		except:
			print("Now that didn't work...")

	def get_url(name):
		string = '"url":'
		name = "pages/" + name + ".txt"
		try:
			with open(name, "r") as file:
				for line in file:
					if string in line:
						url = line.replace("    ", "").replace('"', "").replace(string, "").replace(",", "")
						url = url.replace(" ", "").replace(":", "", 1).replace("\t", "").replace("\n", "")
						url = url.replace("url", "")
						return url
		except:
			print("Now that didn't work...")
	
	type_ = get_type(name)
	headline = get_headline(name)
	created = get_created(name)
	published = get_published(name)
	modified = get_modified(name)
	section = get_section(name)
	creator = get_creator(name)
	good_url = get_url(name)

	return type_, headline, created, published, modified, section, creator, good_url

while True:
	if "ArticleList.csv" in os.listdir():
		table = pd.read_csv("ArticleList.csv", sep = ",")
	else:
		table = pd.DataFrame(columns = [
			"name", "type", "headline", "dateCreated", "datePublished", "dateModified", "articleSection", "creator", "URL"])
	urls = download_sites()
	for url in urls:
		name = url[-12:-5]
		name = name.replace("-", "")
		type_, headline, created, published, modified, section, creator, good_url = get_meta(name)
		df = pd.DataFrame(
			[[name, type_, headline, created, published, modified, section, creator, good_url]],
			columns = [
			"name", "type", "headline", "dateCreated", "datePublished", "dateModified", "articleSection", "creator", "URL"])
		table = table.append(df, ignore_index = True)
		#print("{} parsed and appended to list".format(name))
		#print(table.tail(1))

	print("{} articles have been downloaded so far.".format(len(os.listdir("pages"))))
	table.to_csv(("ArticleList.csv"), sep = ",", index = False)
	print("It's {}, pausing for 10 Minutes.".format(datetime.datetime.now()))
	time.sleep(600)
