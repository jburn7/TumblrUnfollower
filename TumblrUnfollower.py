import pytumblr
import os
from dotenv import load_dotenv 
load_dotenv() 

CONSUMER_PUBLIC=os.getenv("CONSUMER_PUBLIC")
CONSUMER_SECRET=os.getenv("CONSUMER_SECRET")
OLD_CLIENT_TOKEN=os.getenv("OLD_CLIENT_TOKEN")
OLD_CLIENT_SECRET=os.getenv("OLD_CLIENT_SECRET")

oldClient = pytumblr.TumblrRestClient(
  CONSUMER_PUBLIC,
  CONSUMER_SECRET,
  OLD_CLIENT_TOKEN,
  OLD_CLIENT_SECRET
)

_limit = 20

def unfollowStaleBlogs():
	_offset = 1200
	while True:
		print(_offset)
		following = oldClient.following(offset=_offset)
		blogs = following['blogs']
		if blogs == []:
			break
		for blog in blogs:
			if blog['updated'] < 1672604736:
				url = blog['url']
				print('unfollowing' + url)
				oldClient.unfollow(url)
		_offset = _offset + 20

def writeFollowedBlogUrlsToDisk():
	_offset = None
	with open('data/meta.txt', 'r') as file:
		_offset = int(file.readline())

	with open('assets/followed_blogs.txt', 'r+') as file:
		if _offset is None:
			_offset = len(file.readlines())

		while True:
			try:
				following = oldClient.following(limit=_limit, offset=_offset)
				blogs = following['blogs']

				if blogs == []:
					break

				for blog in blogs:
					url = blog['url']
					if(url):
						file.write(url + "\n")

				_offset = _offset + _limit
			except:
				print("limit exceeded, offset=", _offset)
				break

		with open('data/meta.txt', 'w') as metaFile:
			metaFile.write(str(_offset))

writeFollowedBlogUrlsToDisk()
