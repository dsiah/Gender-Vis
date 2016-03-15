import wikipedia as wk
import time, json
from bs4 import BeautifulSoup

if __name__ == '__main__':
	jsfile = json.load(open('dataset/ragged.json'))

	no_finds = []
	success  = []

	for i in jsfile['items']:

		artist = i['track']['artists'][0]['name']
		
		print('# {} by {}'.format(i['track']['name'], artist))
		
		try:
			pg = wk.page(artist)
			soup = BeautifulSoup(pg.html())
			results = soup.find_all("table", class_="infobox")
			print(results)
		except:
			no_finds.append(artist)
			# print('Could not find artist {}'.format(artist))

		time.sleep(.5)
