# long live deletehumanity
#
# NOTE: OUTPUT IS SENT TO THE TERMINAL. THIS ALLOWS FOR GREP / PIPES (ETC)
# TO CREATE A PROXY LIST, SIMPLY USE: python proxygen.py > proxies.txt
import requests
from bs4 import BeautifulSoup
import sys

def getTable(url):
	soup = BeautifulSoup(requests.get(url).content,features='lxml')
	table = soup.find('table')
	try:
		headings = [th.get_text().strip() for th in table.find("tr").find_all("th")]
	except AttributeError:
		exit('[!] Error')
	datasets = []
	for row in table.find_all("tr")[1:]:
	    dataset = dict(zip(headings, (td.get_text() for td in row.find_all("td"))))
	    datasets.append(dataset)
	return datasets

def fplnet(table,https=False):
	addrs = []
	for data in table:
		data = dict(data)
		try:
			if https == True:
				if data[u'Https'] == u'yes':
					addrs.append(data[u'IP Address']+':'+data[u'Port'])
			elif https == False:
				if data[u'Https'] == u'no':
					addrs.append(data[u'IP Address']+':'+data[u'Port'])
			else:
				addrs.append(data[u'IP Address']+':'+data[u'Port'])
		except:
			pass
	return addrs

def nova(table):
	addrs = []
	try:
		for data in table:
			data = dict(data)
			try:
				if 'google' not in data[u'Proxy IP']:
					addrs.append(data[u'Proxy IP'][25:][:5]+data[u'Proxy IP'][45:][:-5]+':'+data[u'Proxy Port'].strip())
			except:
				pass
		return addrs
	except:
		pass

def main():
	if '-h' in sys.argv or '--help' in sys.argv:
		exit('Usage:\n\tpython %s <http/https/(blank for all)>'%(sys.argv[0]))

	if len(sys.argv) > 1:
		https_ = sys.argv[1]
		if https_.lower() == 'https':
			https_ = True
		elif https_.lower() == 'http':
			https_ = False
		else:
			exit('Invalid Argument: '+sys.argv[1])

		proxies = fplnet(getTable('https://www.free-proxy-list.net/'),https_)+fplnet(getTable('https://www.socks-proxy.net/'),https=https_)+fplnet(getTable('https://www.sslproxies.org/'),https=https_)+fplnet(getTable('https://us-proxy.org/'),https=https_)

	else:
		https_ = ''
		proxies = fplnet(getTable('https://www.free-proxy-list.net/'),https=https_) + fplnet(getTable('https://www.socks-proxy.net/'),https=https_)+fplnet(getTable('https://www.sslproxies.org/'),https=https_)+fplnet(getTable('https://us-proxy.org/'),https=https_)+nova(getTable('https://www.proxynova.com/proxy-server-list/'))

	for addr in list(set(proxies)):
		print addr.strip()

if __name__ == '__main__':
	main()
