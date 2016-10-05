from bs4 import BeautifulSoup
import urllib2
import urlparse
import os, sys
import requests
import json

print "Processing...."
def fetch_urls_of_homepage(base_url):
	url_list_with_http = []
	url_list_without_http = []
	html = urllib2.urlopen(base_url)
	soup = BeautifulSoup(html)
	# print soup 
	soup.find('header',id='experiment-header').decompose()
	soup.find('div',class_='breadcrumb').decompose()
	soup.find('footer',class_='footer').decompose()
	soup.head.decompose()
	print soup.prettify()
	for link in soup.find_all('a'):
		pagelinks = str(link.get('href'))
		# print pagelinks
		if pagelinks.startswith('http'):
			url_list_with_http.append(pagelinks)
			# print url_list_with_http
	return url_list_with_http
		# else : 
		# 	url_list_without_http.append(urlparse.urljoin(base_url, pagelinks))
	# return url_list_without_http	


def fetch_homepage_content(final_list):
	for section_link in range(len(final_list)):
		html = requests.get(final_list[section_link])
		soup = BeautifulSoup(html.content)
		# print soup.find('div',class_='content')  
		data = soup.findAll('div',attrs={'class':'content'})
		# print data
		for div in data:
    			links = div.findAll('a')
    			# print links
    		for a in links:
    			pagelinks = str(a.get('href'))
    			a['href'] = urlparse.urljoin(final_list[section_link], pagelinks)
    			                                                                                                    
		sectioncontent = str(soup.find('div',class_='content'))
		# print sectioncontent
		# labspec = json.loads(open('labspec.json', 'r').read())
		# filename = labspec['experiments'][0]['subsections'][section_link]['name'] + '.html'
		labspec = json.loads(open('labspec.json', 'r').read())
		filename1 = labspec['experiments'][0]['name'] +'_'+labspec['experiments'][0]['subsections'][section_link]['name']+'_'+'Unit'+'_'+'html'+'.html'
		filename = filename1.replace(" ","_")
		# print filename
		file = open(filename, 'w')
		try:
			file.write(sectioncontent)
			file.close()
			# break	
		except Exception as e:
			print str(e)

		
def fetch_urls_of_exptpage(url): 
	expt_list_with_http = []
	expt_list_without_http = []
	html = urllib2.urlopen(url)
	soup = BeautifulSoup(html)
	# print soup
	soup.find('header',id='experiment-header').decompose()
	soup.find('div',class_='breadcrumb').decompose()
	soup.find('footer',class_='footer').decompose()
	soup.head.decompose()
	# # print soup.prettify()
	for link in soup.find_all('a'):
		pagelinks = str(link.get('href'))
		if pagelinks.startswith('http'):
			expt_list_with_http.append(pagelinks)
		else : 
			expt_list_without_http.append(urlparse.urljoin(url, pagelinks))
	# print expt_list_without_http
	return expt_list_without_http
	

def fetch_expt_sections_links(url):
	list_with_http = []
	list_without_http = []
	html = urllib2.urlopen(url)
	soup = BeautifulSoup(html) 
	soup.find('header',id='experiment-header').decompose()
	soup.find('div',class_='breadcrumb').decompose()
	soup.find('footer',class_='footer').decompose()
	soup.head.decompose()
	# soup.find('a',class_='sidebar-a').decompose()
	# soup.h2.decompose()
	data = soup.findAll('nav',attrs={'class':'default'})
	# print data
	for div in data:
    		links = div.findAll('a')
    		# print links
    		for a in links:
    			pagelinks = str(a.get('href'))
    			# print pagelinks
			if pagelinks.startswith('http'):
				list_with_http.append(pagelinks)
			else: 
				list_without_http.append(urlparse.urljoin(experiment_links[sectionlink], pagelinks))
				# print list_without_http
	return list_without_http
	        
def fetch_exptspage_content(explinks):
	# dir_name =  "expt" + str(sectionlink)
	# os.mkdir(dir_name)
	# FromRaw = lambda r: r if isinstance(r, unicode) else r.decode('utf-8', 'ignore')
	for section_link in range(len(explinks)):
		html = requests.get(explinks[section_link])
		soup = BeautifulSoup(html.content)
		
		# for links in soup.find_all('a'):
		# 	alinks= str(links.get('href'))
		# 	links['href'] = urlparse.urljoin(explinks[section_link], alinks)
		# 	# print links

		data = soup.findAll('div',attrs={'class':'content'})
		# print data
		for div in data:
    			links = div.findAll('a')
    			# print links
    		for a in links:
    			pagelinks = str(a.get('href'))
    			a['href'] = urlparse.urljoin(explinks[section_link], pagelinks)
		
		sectioncontent = str(soup.find('div',class_='content'))
		# print sectioncontent

		labspec = json.loads(open('labspec.json', 'r').read())
		filename1 = labspec['experiments'][i]['name']+"_"+labspec['experiments'][section_link + 1]['subsections'][section_link]['name']+ "_"+"Unit"+"_"+"html"+'.html'
		filename = filename1.replace(" ","_")
		# filename = labspec['experiments'][section_link + 1]['subsections'][section_link]['name'] + '.html'
		# file = open(os.path.join(dir_name, filename), 'w')
		file = open(filename, 'w')
		try:
			file.write(sectioncontent)
			file.close()
			# break	
		except Exception as e:
			print str(e)


lab_url = "http://bsa-iiith.vlabs.ac.in/"
final_list = fetch_urls_of_homepage(lab_url) 
# print final_list

fetch_homepage_content(final_list)


expt_url = "http://bsa-iiith.virtual-labs.ac.in/index.php?section=List%20of%20experiments"
experiment_links = fetch_urls_of_exptpage(expt_url)
# print experiment_links
i = 0

for sectionlink in range(len(experiment_links)):
	i = i+1
	explinks = fetch_expt_sections_links( experiment_links[sectionlink])
	# print explinks
	# break
	# del explinks[-1]
	# print explinks
	fetch_exptspage_content(explinks)
	# break
    # print "completed generating"


print "completed..!"







