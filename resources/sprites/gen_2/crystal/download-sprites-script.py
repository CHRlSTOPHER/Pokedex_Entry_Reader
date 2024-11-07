# quickly thrown together file to obtain transparent sprites from bulbapedia
# put this file in whichever folder you wish to download sprites into

import requests
import time
from bs4 import BeautifulSoup


SPRITES = {
	# Green Sprites
	1: "https://archives.bulbagarden.net/wiki/Category:Red_and_Green_sprites#/media/File:Spr_1g_001.png",

	# Red and Blue Sprites
	2: "https://archives.bulbagarden.net/wiki/Category:Red_and_Blue_sprites#/media/File:Spr_1b_001.png",

	# Yellow Sprites
	3: "https://archives.bulbagarden.net/wiki/Category:Yellow_sprites#/media/File:Spr_1y_001.png",

	# Silver Sprites Page 1
	4: "https://archives.bulbagarden.net/w/index.php?title=Category:Silver_sprites&fileuntil=%2A195%0ASpr+2s+195.png#mw-category-media",

	# Silver Sprites Page 2
	5: "https://archives.bulbagarden.net/w/index.php?title=Category:Silver_sprites&filefrom=%2A195%0ASpr+2s+195.png#mw-category-media",

	# Gold Sprites Page 1
	6: "https://archives.bulbagarden.net/w/index.php?title=Category:Gold_sprites&fileuntil=%2A196%0ASpr+2g+196.png#mw-category-media",

	# Gold Sprites Page 2
	7: "https://archives.bulbagarden.net/w/index.php?title=Category:Gold_sprites&filefrom=%2A196%0ASpr+2g+196.png#mw-category-media",

	# Crystal Sprites Page 1
	8: "https://archives.bulbagarden.net/w/index.php?title=Category:Crystal_sprites&fileuntil=%2A200%0ASpr+2c+200.png#mw-category-media",

	# Crystal Sprites Page 2
	9: "https://archives.bulbagarden.net/w/index.php?title=Category:Crystal_sprites&filefrom=%2A200%0ASpr+2c+200.png#mw-category-media"
}

# modify this number to sprite version
GAME_VERSION = 9

image_url = SPRITES[GAME_VERSION]

# call the database and get the contents of the html
img_data = requests.get(image_url).content

image_sources = []

# find all the png classes in the html data
soup = BeautifulSoup(img_data)
image_list = soup.find_all('img')
for image in image_list:
	# the src element contains the url directly to the png
	image_source = image['src']
	# look for a keyword to append only uploaded sprites
	if "upload" in image_source:
		image_sources.append(image_source)

dex_num = 1
for url in image_sources:
	image = requests.get(url).content
	# grabbing the dex num from url helps avoid duplicate issues.
	dex_num = url[-7:-4]
	with open(f"0{dex_num}.png", 'wb') as handler:
		time.sleep(0.5)
		handler.write(image)
