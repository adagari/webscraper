#!/usr/bin/env python
try:
	from bs4 import BeautifulSoup
	from urllib.parse import urljoin
	import requests, re, hashlib, os
except:
	print("Please install packages found in requirements.txt")
	
def main():
	url             = set_variables()
	response        = check_response_code(url)
	link_list       = scrape_url(url, response)
	unique_links    = get_unique_url(link_list)
	validated_links = validate_unique_links(unique_links)
	output_csv(validated_links)
	exit()

def set_variables():
	url = 'http://www.census.gov/programs-surveys/popest.html'
	print("The current url is set to: " + url)
	return url

def check_response_code(url):
	print("Checking HTTP response.")
	response = requests.get(url)
	if response.status_code == 200:
		print("The request has succeeded.")
		return response
	else:
		answer = input("The request has failed. Do you want to try again? (Y/N)")
		if answer.upper() == 'Y':
			main()
		else:
			exit()
			
def scrape_url(url, response):
	relative_links = []
	absolute_links = []
	soup = BeautifulSoup(response.text, "html.parser")
	for i in soup.findAll('a', href=True):
		if not i['href'].startswith('http'):
			relative_links.append(i['href'])
		else:
			absolute_links.append(i['href'])
	print("The total number of relative links: " + str(len(relative_links)))
	print("The total number of absolute links: " + str(len(absolute_links)))
	print("Resolving relative links to their absoulte path.")
	for i in relative_links:
		absolute_links.append(urljoin(url, i))
	return absolute_links
	
def get_unique_url(link_list):
	unique_link_list = []
	print("Removing duplicate links found.")
	for i in link_list:
		if i not in unique_link_list:
			unique_link_list.append(i)
	print("The number of unique links scraped: " + str(len(unique_link_list)))
	return unique_link_list
	
def validate_unique_links(unique_links):
	webpage_hash_list   = []
	validated_link_list = []
	print("Ensuring only unique webpages are returned from unique links.")
	print("This may take a moment...")
	for i in unique_links:
		response = requests.get(i)
		if response.status_code == 200:
			try:
				web_page = requests.get(i)
				web_hash = hashlib.md5(web_page.text.encode('utf-8')).hexdigest()
				if web_hash not in webpage_hash_list:
					webpage_hash_list.append(web_hash)
					validated_link_list.append(i)
			except:
				print(i + ", failed hash validation check.")
				validated_link_list.append(i)
		else:
			print(i + ", failed status code check, but will be included.")
	print("The number of validated unique links scraped: " + str(len(validated_link_list)))
	return validated_link_list

def output_csv(validated_links):
	file_name = 'output.csv'
	print("Writing URIs to " + file_name + ".")
	with open(file_name, 'w') as f:
		f.write('Unique URIs' + '\n')
		for i in validated_links:
			f.write(i + '\n')
	print("Listing files in directory.")
	os.system('ls')
	
if __name__ == "__main__":
	os.system('clear')
	main()