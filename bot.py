from requests import post
from os import getenv
from time import strftime, gmtime
from time import sleep
from emailslib import gen_message, send_email
import schedule

# Environment variables
# SMTPUSR -	The user that sends the emails
# EMAIL - 	The email address of the recipient
# SMTPPWD -	The authentication password for the sender
# USER - 	The username of the HelioHost account
# PWD - 	The password of the HelioHost account
# REPEAT -	Repeat the login every Monday


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


def send_report_email(cookie_response, login_time=None):
	send_email(
		getenv("SMTPUSR"),
		getenv("EMAIL"),
		getenv("SMTPPWD"),
		gen_message(
			"Email Reports <%s>" % getenv("SMTPUSR"),
			getenv("EMAIL"),
			"HelioHost Auto Login Bot - Report",
			"""Hello there!

Thanks for using the HelioHost Auto Login Bot!

We recently{time} attempted a login into your account.

Here is your session cookie for Heliohost:
{cookies}

Sincerely,
Heliohost Auto Login Bot.

--------------------------------

This message was sent to {receiver} from {source} because you subscribed to the email notifications.
If this action was not requested by you, please discard this email and DO NOT use the confidential data included in the email.
""" \
			.format(
				cookies=cookie_response.strip(),
				time=(" (%s)" % strftime('%Y-%m-%dT%H:%M:%SZ', login_time) if login_time is not None else ''),
				receiver=getenv("EMAIL"),
				source=getenv("SMTPUSR")
			)
		)
	)


def automatic_execution():
	now = gmtime()
	print(f"Script running @ {strftime('%Y-%m-%dT%H:%M:%SZ', now)} ...")
	cookie_response = run(getenv("USER"), getenv("PWD"))
	print(cookie_response[0:11])
	# Don't print too much information to the console, because unauthorized eyes might see it
	if getenv("EMAIL"):
		print(f"Sending email to {getenv('EMAIL')}")
		send_report_email(cookie_response, login_time=now)
	else:
		print(
			"No EMAIL environment variable specified.",
			"Not sending any emails.",
			sep='\n'
		)

def run_repeatedly():
	schedule.every().monday.at("16:00").do(automatic_execution)
	while True:
		schedule.run_pending()
		sleep(1)

if getenv("REPEAT"):
	run_repeatedly()
elif __name__ == '__main__':
	run(getenv("USER"), getenv("PWD"))
