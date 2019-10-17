import requests as rq
import webbrowser

def history_contains(response, code):
	for x in response.history:
		if (x.status_code == code):
			return True

	return False

def page_contains(response, text):
	if text in response.text:
		return True
	return False



def run(sites):
	used_sites = {}
	get_failed = True

	for address in sites:
		used_sites[address] = None
		try:
			r = rq.get(address)
			url = address
			get_failed = False
			used_sites[address] = r.status_code

			break
		except rq.exceptions.ConnectionError as errc:
		    print ("Connection Error:",errc)
		except rq.exceptions.Timeout as errt:
		    print ("Timeout Error:",errt)
		except rq.exceptions.RequestException as err:
		    print ("Check network status:",err)

	if get_failed: exit(1)

	if history_contains(r, 302):
		print("You need to log-in! Your network is captive.")
		used_sites[url] = 302
		webbrowser.open(url)
	elif (r.status_code == 200) & page_contains(r, sites.get(url)):
		print("Network Libertad!")
	else:
		print("Check network connection")

	for site in used_sites:
		print("URL ", site, " returned code: ", used_sites.get(site))


if __name__ == '__main__':
	sites = {"http://captive.apple.com": "Success"}
	run(sites)