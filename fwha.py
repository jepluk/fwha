import requests as r, re, os
from bs4 import BeautifulSoup as bs

H = '\x1b[38;5;48m'; M = '\x1b[38;5;196m'; P = '\x1b[38;5;255m'; L = '\x1b[38;5;2m'; J = '\x1b[38;5;171m'
def scrapDomain(ses, domain = []):
    web = bs(ses.get('https://www.freewebhostingarea.com/').text, 'html.parser')
    for domain_option in web.find_all('option'):
        if domain_option['value'] == 'Select': continue

        domain_name = domain_option.text
        domain.append(domain_name)

    return domain

def request(ses, hostname, domain):
    data = {'action':'check_domain', 'domain':domain, 'thirdLevelDomain':hostname}
    web = bs(ses.post('https://www.freewebhostingarea.com/cgi-bin/create_account.cgi', data=data).text, 'html.parser')
    
    url = hostname +'.'+ domain
    if f'{url} already created' in web.text: print(f'{P}{url}{M} Sudah didaftarkan, coba hostname lain')
    elif 'is available' in web.text:
        domain_name = re.search('input name="domainName" type="hidden" value="(.*?)"', str(web)).group(1)
        print(f'{P}{domain_name}{H} is avalibe')
        mail = input(f'\n{P}Email ({M}@gmail.com{P}): {H}')
        passw = input(f'{P}Password ({M}length 6+{P}): {H}')
        data = {'action':'validate','email':mail ,'domainName': domain_name, 'password': passw, 'confirmPassword': passw, 'agree':'1'}

        web = bs(ses.post('https://newserv.freewha.com/cgi-bin/create_ini.cgi', data=data).text, 'html.parser')
        if 'was successfully activated. Your address is' in web.text: print(f'\n{M} >{H} BERHASIL AKTIFASI\n{M} >{P} FTP Server/Host: {J}{url}\n{M} >{P} FTP Login/Username: {J}{url}\n{M} >{P} Password: {J}{passw}\n{M} >{P} Control panel: {J}{url}/cpanel\n{M} >{P} FTP Client: {J}{url}/ftp/')
        else: print(f'{M}Gagal aktivasi hostname {P}{url}')

    elif 'Invalid domain name format' in web.text: print(url +'Invalid domain name format')
    else:
        prinr(web)

if __name__ == "__main__":
    os.system('clear')
    session = r.session()
    session.headers.update({'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'id-ID,id;q=0.9', 'Content-Type': 'application/x-www-form-urlencoded', 'Origin': 'https://www.freewebhostingarea.com', 'Referer': 'https://www.freewebhostingarea.com/', 'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not=A?Brand";v="24"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-User': '?1', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5666.197 Safari/537.36'})

    domain_list = scrapDomain(session)
    print(f'{P}Domain yang tersedia: {L}{domain_list}')
    url = input(f'\n{P}Masukan hostname ({M}ex: errucha.6te.net{P}): {H}')

    domain = [dom for dom in domain_list if re.search(fr'\b{re.escape(dom)}\b', url)]
    if domain: request(session, url.split('.')[0], domain[0])
    else: print(f'{P}{domain_name[0]}{M} Tidak valid')
