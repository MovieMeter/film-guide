from bs4 import BeautifulSoup
import sys
import requests
from fake_useragent import UserAgent


def get_review(movie):
	proxies = {
		'http':'http://10.11.0.1:8080',
		'https':'http://10.11.0.1:8080'
	}
	# ua=UserAgent()
	header={ 'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
	print(requests.get('http://ipecho.net/plain').text)

	# exit()

	# movie=input('Enter movie? ')
	movier= movie+" New York Times review"
	addr='https://www.google.co.in/search?'
	param={'q':movier,'oq':movier}
	print('Getting review..')
	r=requests.get(addr,params=param,headers=header)



	soup=BeautifulSoup(r.content,'lxml')
	url=soup.find('div',class_='rc')
	url=url.a['href']
	r2=requests.get(url,headers=header)
	soup2=BeautifulSoup(r2.content,'lxml')
	tag=""
	count=0
	for item in soup2.find_all('p',class_="story-body-text story-content"):
		count=1
		tag=tag+item.get_text()
		tag=tag+'\n'
	# 	"""while soup2.find('p',class_="story-body-text story-cont")!=None:
	#
	# 	temp=soup2.find('p',class_="story-body-text story-content")
	# 	print temp
	# 	tag=temp.get_text()
	# 	tag=tag+'\n'
	# 	for item in soup2.temp.next_siblings:
	# 		if item.find('p',class_="story-body-text story-content")!=None:
	# 			tag=tag+item.get_text()
	# 			tag=tag+'\n'
	# 		else:
	# 			break
	# else:"""
	if count ==0:
		for item in soup2.find_all('p'):
			if item.br==None:
				tag=tag+item.get_text()
				tag=tag+'\n'

		# '''temp=soup2.find('div', class_="timestamp_print")
		# for item in soup2.temp.next_siblings:
		# 	if item.p!=None:
		# 		tag=tag+item.get_text()
		# 		tag=tag+'\n'''
	# tag=tag.encode('ascii','ignore')
	return str(tag)

# fp=open("review.txt", 'w')
# fp.write(str(tag))
# fp.close()
#print tag



# params2={'q':movie+" movie",'oq':movie+" movie"}
# print('Done.\nGetting info..')
# r3=requests.get(addr,params=params2,headers=header, proxies=proxies)
# soup3=BeautifulSoup(r3.content,'lxml')

# mname=soup3.find(class_="_Q1n")
# fp.write('\n \n' + mname.get_text().encode('ascii','ignore').strip())

# boxlist=soup3.find_all("a",class_="_hvg kno-fb-ctx")
# print boxlist 
# imdb=boxlist[0].get_text().encode('ascii','ignore')
# imdb_rate=imdb.partition('I')
# #print imdb_rate
# fp.write('\n'+imdb_rate[0])
# rot=boxlist[1]['href']
# #print rot
# r4=requests.get(rot,headers=header, proxies=proxies)
# soup4=BeautifulSoup(r4.content,'lxml')
# rotscore=soup4.find('div',id="scoreStats")
# #print rotscore.div.get_text().strip()
# rotscore=rotscore.div.get_text().strip()
# rotscore=rotscore.partition(':')
# rotscore=rotscore[2].encode('ascii','ignore').strip()
# #print rotscore
# fp.write('\n'+"rotten score:\t"+rotscore)

# info=soup4.find('ul',class_="content-meta info").find_all('li')
# genre=info[1].get_text().strip()
# genre=genre.partition(':')[2].strip()
# direct=info[2].get_text().strip()
# direct=direct.partition(':')[2].strip()
# #print genre+'\n'+direct
# fp.write('\n'+"genre:  "+genre+'\n'+"directed by:  "+direct)
# metascore=boxlist[2].get_text().encode('ascii','ignore')
# #print metascore
# fp.write('\n'+metascore)
# paramcast={'q':movie+" cast imdb", 'oq':movie+ " cast imdb"}
# r5=requests.get(addr,params=paramcast,headers=header, proxies=proxies)
# soup5=BeautifulSoup(r5.content,'lxml')
# #print r5.url
# casturl=soup5.find("div" ,class_="rc")
# #print casturl.a['href']
# r6=requests.get(casturl.a['href'],headers=header, proxies=proxies)
# soup6=BeautifulSoup(r6.content,'lxml')
# index=0
# actor=list()
# character=list()
# for item in soup6.find_all('span',class_="itemprop"):
# 	actor.append(item.get_text().encode('ascii','ignore'))
# 	index+=1
# 	if index>=9:
# 		break
# index=0
# for item in soup6.find_all('td',class_="character"):
# 	character.append(item.get_text().encode('ascii','ignore'))
# 	index+=1
# 	if index>=9:
# 		break
# for index in range(0,len(actor)):
# 	fp.write('\n'+actor[index]+'\t'+ character[index]+'\n')
# fp.close()

