from urllib.request import urlopen
from bs4 import BeautifulSoup

ROOT_URL = 'http://www.bbc.co.uk'

def download_media(media):
    print("reading:", ROOT_URL+media['link'])
    try: 
        html = urlopen(ROOT_URL+media['link']).read()
    except:
        print("Failed...")
        err_file = open('err_log.log', 'a+')
        err_file.write(media['link'])
        err_file.close()
        return
    soup = BeautifulSoup(html, 'html.parser')
    soup = soup.find("div", {"role": "article"})
    pdf_link = soup.find("a", {"class": "bbcle-download-extension-pdf"})
    mp3_link = soup.find("a", {"class": "bbcle-download-extension-mp3"})
        
    #pdf download
    print()
    print("downloading PDF...")
    try:
        with urlopen(pdf_link['href']) as f_1:
            with open('./../download/pdf/Episode_' + media['episode'] + '_' + media['title'] + '.pdf', 'wb') as i_f_1:
                img = f_1.read()
                i_f_1.write(img)
                print("Success")
    except:
        print("Failed...")
        err_file = open('err_log.log', 'a+')
        err_file.write(media['link'])
        err_file.close()
    #mp3 download
    print()
    print("downloading MP3...")
    try:
        with urlopen(mp3_link['href']) as f_2:
            with open('./../download/mp3/Episode_' + media['episode'] + '_' + media['title'] + '.mp3', 'wb') as i_f_2:
                img = f_2.read()
                i_f_2.write(img)
                print("Success")
    except:
        print("Failed...")
        err_file = open('err_log.log', 'a+')
        err_file.write(media['link'])
        err_file.close()

    print()

    return

# main code
print("start:", ROOT_URL+'/learningenglish/english/features/6-minute-english')
html =  urlopen(ROOT_URL+'/learningenglish/english/features/6-minute-english').read()
soup = BeautifulSoup(html, 'html.parser')
media_soup = soup.find_all("li", {"class": "course-content-item"})
media_list = []
for sp in media_soup:
    media_list.append({
            "link": sp.find("h2").find("a")['href'],
            "title": sp.find("h2").find("a").string.strip().replace(" ", "_").replace("?", "").replace("'", "").replace(":", "_"),
            "episode": sp.find("h3").find("b").string.strip().replace("Episode ", "")
        })

total_count = len(media_list)
print("Total Count:", total_count)
print()
print("download start...")

# open each media and download
n = 0 
for media in media_list:
    n += 1
    print(n, "/", total_count)
    download_media(media)
