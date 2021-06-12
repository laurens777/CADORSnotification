import requests
from bs4 import BeautifulSoup as bs
from time import sleep
import smtplib, ssl

def main(ID):
    lastYear = ID.split('P')[0]
    lastID = ID.split('P')[1]
    regis = ["GGMA", "GIUK"]
    returnID = ID
    new = []

    for registration in regis:
        my_session = requests.session()
        for_cookies = my_session.get("https://wwwapps.tc.gc.ca/saf-sec-sur/2/cadors-screaq/ql.aspx?cno%3d%26dtef%3d%26dtet%3d2021-06-10%26otp%3d-1%26ftop%3d%253e%253d%26ftno%3d0%26ijop%3d%253e%253d%26ijno%3d0%26olc%3d%26prv%3d-1%26rgn%3d-1%26tsbno%3d%26tsbi%3d-1%26arno%3d%26ocatno%3d%26ocatop%3d1%26oevtno%3d%26oevtop%3d1%26evtacoc%3d3%26fltno%3d%26fltr%3d-1%26cars%3d-1%26acat%3d-1%26nar%3d%26aiddl%3d-1%26aidxt%3d%26optdl%3d-1%26optcomt%3d%26optseq%3d%26optxt%3d%26opdlxt%3dResults%2bwill%2bappear%2bin%2bthis%2blist%26mkdl%3d-1%26mkxt%3d%26mdldl%3d-1%26mdlxt%3d%26cmkdl%3dC%26cmkxt%3d" + registration)
        my_cookies = for_cookies.cookies
        my_headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'}
        response = my_session.get("https://wwwapps.tc.gc.ca/saf-sec-sur/2/cadors-screaq/ql.aspx?cno%3d%26dtef%3d%26dtet%3d2021-06-10%26otp%3d-1%26ftop%3d%253e%253d%26ftno%3d0%26ijop%3d%253e%253d%26ijno%3d0%26olc%3d%26prv%3d-1%26rgn%3d-1%26tsbno%3d%26tsbi%3d-1%26arno%3d%26ocatno%3d%26ocatop%3d1%26oevtno%3d%26oevtop%3d1%26evtacoc%3d3%26fltno%3d%26fltr%3d-1%26cars%3d-1%26acat%3d-1%26nar%3d%26aiddl%3d-1%26aidxt%3d%26optdl%3d-1%26optcomt%3d%26optseq%3d%26optxt%3d%26opdlxt%3dResults%2bwill%2bappear%2bin%2bthis%2blist%26mkdl%3d-1%26mkxt%3d%26mdldl%3d-1%26mdlxt%3d%26cmkdl%3dC%26cmkxt%3d" + registration, headers=my_headers, cookies=my_cookies)
        soup = bs(response.content, 'html.parser')
        div = soup.find_all('div', attrs={'class': 'col-md-2 mrgn-bttm-md align-center mrgn-tp-sm'})
        for d in div:
            if d.find('a'):
                incidentYear = d.find('a').text.split('P')[0]
                incidentID = d.find('a').text.split('P')[1]
                if incidentYear >= lastYear and incidentID > lastID:
                    new.append(d.find('a')['href'])
                    if incidentID > returnID.split('P')[1]:
                        returnID = d.find('a').text
                else:
                    continue

    if new:
        port = 465
        password = ""

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login("", password)
            message = "Subject: New CADORS! \n\nThere is a new CADORS involving club aircraft. \nlink: https://wwwapps.tc.gc.ca/Saf-Sec-Sur/2/cadors-screaq/" + new[0]
            server.sendmail("", "", message)

    return returnID
            

if __name__ == "__main__":
    lastID = "2021P0469"
    while True:
        lastID = main(lastID)
        print(lastID)
        sleep(60*60*4)