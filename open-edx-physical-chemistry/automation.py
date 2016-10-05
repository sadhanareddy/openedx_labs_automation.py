from bs4 import BeautifulSoup
import urllib2
import urlparse
import os, sys
import requests
import json

print "Processing...."
def fetch_urls_of_homepage(base_url):
	url_list= []
	html = urllib2.urlopen(base_url)
	soup = BeautifulSoup(html, "html5lib")
	soup.find('header',id='experiment-header').decompose()
	soup.find('div',class_='breadcrumb').decompose()
	soup.find('footer',class_='footer').decompose()
	soup.head.decompose()
	data = soup.findAll('nav',attrs={'class':'default'})
	for nav in data:
		links = nav.findAll('a')
		for a in links:
			pagelinks = str(a.get('href'))
			if pagelinks.startswith("http"):
				url_list.append(pagelinks)
			else:
				url_list.append(urlparse.urljoin(base_url, pagelinks))
	return url_list	


def fetch_homepage_content(final_list):
	for section_link in range(len(final_list)):
		html = requests.get(final_list[section_link])
		soup = BeautifulSoup(html.content, "html5lib") 
		data = soup.findAll('div',attrs={'class':'content'})
		for div in data:
    			links = div.findAll('a')
    		for a in links:
    			pagelinks = str(a.get('href'))
    			if pagelinks.startswith('http'):
    				a['href'] = pagelinks
    			else:
    				a['href'] = urlparse.urljoin(final_list[section_link], pagelinks)
    			                                                                                                    
		sectioncontent = str(soup.find('div',class_='content'))
		labspec = json.loads(open('labspec.json', 'r').read())
		filename1 = labspec['experiments'][0]['name'] +'_'+labspec['experiments'][0]['subsections'][section_link]['name']+'_'+'Unit'+'_'+'html'+'.html'
		filename = filename1.replace(" ","_")
		file = open(filename, 'w')
		try:
			file.write(sectioncontent)
			file.close()
		except Exception as e:
			print str(e)


def fetch_urls_of_exptpage(url): 
	expts_url_list = []
	html = urllib2.urlopen(url)
	soup = BeautifulSoup(html,"html5lib")
	soup.find('header',id='experiment-header').decompose()
	soup.find('div',class_='breadcrumb').decompose()
	soup.find('footer',class_='footer').decompose()
	soup.head.decompose()
	data = soup.findAll('div',attrs={'class':'content'})
	for div in data:
		links = div.findAll('a')
		for a in links:
			pagelinks = str(a.get('href'))
			if pagelinks.startswith("http"):
				expts_url_list.append(pagelinks)
			else:
				expts_url_list.append(urlparse.urljoin(url, pagelinks))
	return expts_url_list
	

def fetch_expt_sections_links(url):
	url_list = []
	html = urllib2.urlopen(url)
	soup = BeautifulSoup(html, "html5lib") 
	soup.find('header',id='experiment-header').decompose()
	soup.find('div',class_='breadcrumb').decompose()
	soup.find('footer',class_='footer').decompose()
	soup.head.decompose()
	data = soup.findAll('nav',attrs={'class':'default'})
	for nav in data:
		links = nav.findAll('a')
		for a in links:
			pagelinks = str(a.get('href'))
			url_list.append(urlparse.urljoin(url, pagelinks))
	return url_list	

	        
def fetch_exptspage_content(explinks):
	for section_link in range(len(explinks)):
		html = requests.get(explinks[section_link])
		soup = BeautifulSoup(html.content, "html5lib")
		
		data = soup.findAll('div',attrs={'class':'content'})
		for div in data:
    		        links = div.findAll('a')
    		        for a in links:
    			        pagelinks = str(a.get('href'))
    			        a['href'] = urlparse.urljoin(explinks[section_link], pagelinks)
    			        for div in data:
    				        links1 = div.findAll('img')
    				        for img in links1:
    					        imglinks = img.get('src')
    					        if imglinks.startswith('http'):
    						        img['src'] = imglinks
    					        else:
    						        img['src'] = urlparse.urljoin(explinks[section_link], imglinks)
    			                                                                                                    
		sectioncontent = str(soup.find('div',class_='content'))
		labspec = json.loads(open('labspec.json', 'r').read())
		filename1 = labspec['experiments'][i]['name']+"_"+labspec['experiments'][i]['subsections'][section_link]['name']+ "_"+"Unit"+"_"+"html"+'.html'
		filename = filename1.replace(" ","_")
		file = open(filename, 'w')
		try:
			file.write(sectioncontent)
			file.close()	
		except Exception as e:
			print str(e)


lab_url = "http://ccnsb06-iiith.vlabs.ac.in/"
final_list = fetch_urls_of_homepage(lab_url) 

fetch_homepage_content(final_list)


expt_url = "http://ccnsb06-iiith.vlabs.ac.in/index.php?section=Experiments"
experiment_links = fetch_urls_of_exptpage(expt_url)

for sectionlink in range(len(experiment_links)):
	i = sectionlink + 1
	explinks = fetch_expt_sections_links( experiment_links[sectionlink])
	fetch_exptspage_content(explinks)
print "completed..!"







