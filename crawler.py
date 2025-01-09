from requests_tor import RequestsTor
from bs4 import BeautifulSoup
import re
import requests

# Initialize RequestsTor
rt = RequestsTor()

# Read onion links from fileimport requestssoup
base_search_url = ['http://hqfld5smkr4b4xrjcco7zotvoqhuuoehjdvoin755iytmpk4sm7cbwad.onion', 'http://s4k4ceiapwwgcm3mkb6e4diqecpo7kvdnfr5gg7sph7jjppqkvwwqtyd.onion', 'http://guzjgkpodzshso2nohspxijzk5jgoaxzqioa7vzy6qdmwpz3hq4mwfid.onion', 'http://prjd5pmbug2cnfs67s3y65ods27vamswdaw2lnwf45ys3pjl55h2gwqd.onion', 'http://s57divisqlcjtsyutxjz2ww77vlbwpxgodtijcsrgsuts4js5hnxkhqd.onion', 'http://s4k4ceiapwwgcm3mkb6e4diqecpo7kvdnfr5gg7sph7jjppqkvwwqtyd.onion', 'http://paavlaytlfsqyvkg3yqj7hflfg5jw2jdg2fgkza5ruf6lplwseeqtvyd.onion', 'http://zqktlwiuavvvqqt4ybvgvi7tyo4hjl5xgfuvpdf6otjiycgwqbym2qad.onion', 'http://2jwcnprqbugvyi6ok2h2h7u26qc6j5wxm7feh3znlh2qu3h6hjld4kyd.onion', 'http://jgwe5cjqdbyvudjqskaajbfibfewew4pndx52dye7ug3mt3jimmktkid.onion', 'http://55niksbd22qqaedkw36qw4cpofmbxdtbwonxam7ov2ga62zqbhgty3yd.onion', 'http://s57divisqlcjtsyutxjz2ww77vlbwpxgodtijcsrgsuts4js5hnxkhqd.onion', 'http://y22arit74fqnnc2pbieq3wqqvkfub6gnlegx3cl6thclos4f7ya7rvad.onion', 'http://hqfld5smkr4b4xrjcco7zotvoqhuuoehjdvoin755iytmpk4sm7cbwad.onion', 'http://ovai7wvp4yj6jl3wbzihypbq657vpape7lggrlah4pl34utwjrpetwid.onion', 'http://xykxv6fmblogxgmzjm5wt6akdhm4wewiarjzcngev4tupgjlyugmc7qd.onion', 'http://wk3mtlvp2ej64nuytqm3mjrm6gpulix623abum6ewp64444oreysz7qd.onion', 'http://odahix2ysdtqp4lgak4h2rsnd35dmkdx3ndzjbdhk3jiviqkljfjmnqd.onion', 'http://qazkxav4zzmt5xwfw6my362jdwhzrcafz7qpd5kugfgx7z7il5lyb6ad.onion', 'http://mp3fpv6xbrwka4skqliiifoizghfbjy5uyu77wwnfruwub5s4hly2oid.onion', 'http://p2qzxkca42e3wccvqgby7jrcbzlf6g7pnkvybnau4szl5ykdydzmvbid.onion', 'http://prjd5pmbug2cnfs67s3y65ods27vamswdaw2lnwf45ys3pjl55h2gwqd.onion', 'http://rxmyl3izgquew65nicavsk6loyyblztng6puq42firpvbe32sefvnbad.onion', 'http://vhlehwexxmbnvecbmsk4ormttdvhlhbnyabai4cithvizzaduf3gmayd.onion', 'http://ymvhtqya23wqpez63gyc3ke4svju3mqsby2awnhd3bk2e65izt7baqad.onion', 'http://k6m3fagp4w4wspmdt23fldnwrmknse74gmxosswvaxf3ciasficpenad.onion', 'http://lqcjo7esbfog5t4r4gyy7jurpzf6cavpfmc4vkal4k2g4ie66ao5mryd.onion']


up = open("uptime-links.txt", "a")
down = open("downtime-links.txt", "a")
for base in base_search_url:
	
	rt.check_ip()
	rt.new_id()
	#rt.test()
	r = rt.get(base)

	soup = BeautifulSoup(r.text,"html.parser")

	onion_links = re.findall(r"http://[A-Za-z0-9]{56}.onion",soup.get_text())
	print(f"[*]Total links scraped from {base} is {len(onion_links)}")
	#print("******Checking Status of these links*****")
	
	for onion in onion_links:
		try:
			check_url =  rt.get(onion)
			if check_url.status_code == 200:
				print(f"UP - {check_url.status_code} - {onion}")
				up.write(f"{onion}")
		except:
			print(f"DOWN - {onion} ")
			down.write(f"{onion}")
	
up.close()
down.close()
