from requests import post
from os import getenv

def run(username: str,
		password: str,
		user_agent: str="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
		) -> str:
	r = post(
		"https://www.heliohost.org/login/",
		headers={
			"Cache-Control": "max-age=0",
			"Upgrade-Insecure-Requests": "1",
			"Origin": "https://www.heliohost.org",
			"Content-Type": "application/x-www-form-urlencoded",
			"User-Agent": user_agent,
			"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
			"Sec-Fetch-Site": "same-origin",
			"Sec-Fetch-Mode": "navigate",
			"Sec-Fetch-User": "?1",
			"Sec-Fetch-Dest": "document",
			"Referer": "https://www.heliohost.org/",
			"Accept-Encoding": "gzip, deflate, br",
			"Accept-Language": "en-US,en;q=0.9"
		},
		data={
			"email": username,
			"password": password
		}
	)
	cookies = r.headers.get('Set-Cookie')
	print(cookies)


if __name__ == '__main__':
	run(getenv("USER"), getenv("PWD"))
