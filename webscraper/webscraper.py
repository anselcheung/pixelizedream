import requests
from selenium import webdriver
import time
import os

def pinterest_scrape(search):
    search = search.replace(' ', '%20')

    link = "https://www.pinterest.com/search/pins/?q={}&rs=typed".format(search)
    driver = webdriver.Chrome()
    driver.get(link)
    time.sleep(3)

    image_links = []
    change_flag = True
    while change_flag:
        change_flag = False
        images = driver.find_elements_by_css_selector("div.XiG.zI7.iyn.Hsu>div.Pj7.sLG.XiG.ho-.m1e>div.XiG.zI7.iyn.Hsu>img.hCL.kVc.L4E.MIw")
        for i in images:
            src = i.get_attribute('src')
            if src not in image_links:
                image_links.append(src)
                change_flag = True
        
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(15)
    
    driver.close()
    search = search.replace('%20', '_')
    print(f"Found {len(image_links)} images, downloading now to F:/pinterest_scrape/{search}")
    if not os.path.exists(f"F:/pinterest_scrape/{search}"):
        os.makedirs(f"F:/pinterest_scrape/{search}")
    success = 0
    for i in range(len(image_links)):
        link = image_links[i]
        try:
            img_data = requests.get(link).content
            with open(f"F:/pinterest_scrape/{search}/{search}_{i}.jpg", 'wb') as handler:
                handler.write(img_data)
            success += 1
        except:
            pass
    print(f"Downloaded {success} images to F:/pinterest_scrape/{search}")

if __name__=='__main__':
    searches = ['pixel game aesthetic']
    for search in searches:
        pinterest_scrape(search)