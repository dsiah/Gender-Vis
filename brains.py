import urllib2, json
import musicbrainzngs as mbs

from time import sleep
from bs4  import BeautifulSoup

mbs.set_useragent('GenderVis', 1.0)

def mbs_query(artist_name):
	# Get Music Brains ID of artist for specific query
	mid  = mbs.search_artists(artist_name)['artist-list'][0]['id']
	sleep(1) # Rate limit one per second
	return mbs.get_artist_by_id(mid)['artist']

def group_members(artist_id):
	url     = 'https://musicbrainz.org/artist/{}/relationships'.format(artist_id)
	soup    = BeautifulSoup(urllib2.urlopen(url).read(), 'html.parser')
	text    = soup.find_all('th', string='members:')[0].find_next()
	members = text.find_all('a')

	return { p.text: p['href'] for p in members }

def complete_info(mbs_artist):
	artists = {}
	# If artist is group run group_members
	print('{} is the artist obj'.format(mbs_artist))
	if mbs_artist['type'] != 'Person':
		members = group_members(mbs_artist['id'])

		for member in members:
			# Lookup artist by id and get gender
			midx   = members[member].rfind('/')
			sleep(1) # Rate limit one per second
			person = mbs.get_artist_by_id(members[member][midx + 1:])
			artists[member] = person['artist']['gender']
	else:
		print('Extracting gender of {}'.format(mbs_artist))
		artists[mbs_artist['name']] = mbs_artist['gender']

	return artists


if __name__ == '__main__':
	success, no_finds = [], []

	jsfile = json.load(open('dataset/ragged.json'))

	for i in jsfile['items'][4:8]:
		artist = i['track']['artists'][0]['name']
		
		print('# {} by {}'.format(i['track']['name'], artist))

		try:
			res = mbs_query(artist)
			suc = complete_info(res)
			print(suc)
			success.append(suc)

		except:
			no_finds.append(artist)
			print('Could not find artist {}'.format(artist))