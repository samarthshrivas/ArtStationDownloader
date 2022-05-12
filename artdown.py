import os 
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import urlparse
import cloudscraper
import time
from concurrent import futures
from multiprocessing import cpu_count
import requests
root_path = "ArtStation"

max_workers = cpu_count()*4
# print("max_workers: ",max_workers)
executor = futures.ThreadPoolExecutor(max_workers)
futures = []

# root_path = "Wall\ARTs"

# url = f"https://{username}.artstation.com"


def rget(url):
    try:
        return requests.get(url)
    except Exception as e:
        print(e)
        print(url)


def download(url, path, filename):
    if not os.path.exists(path):
        os.makedirs(path)
    if not os.path.exists(f"{path}/{filename}"):
        with open(f"{path}/{filename}", 'wb') as local_file:
            try:
                local_file.write(requests.get(url).content)
                print(f"[DOWNLOADED] {url} '{path}/{filename}'")
            except:
                pass
    elif os.path.exists(f"{path}/{filename}"):
        print(f"[EXISTS][SKIPPED] {url} '{path}/{filename}'")


def get_proj_img(lis):
    """ takes a list of projects href and returns a dict of name of project and list of images
        {proj1:[img1,img2,img3]}    
    """
    d = {}
    for i in lis:
        soup = BeautifulSoup(rget("https://www.artstation.com"+i), 'html.parser')
        print(soup.json)


def get_projects(username):
    lis = []
    page = 0
    print(f'\n==========[{username}] BEGIN==========')
    while True:
        page  += 1
        print(f'\n==========Get page {page}==========')
        soup = BeautifulSoup(rget(f'https://{username}.artstation.com/rss?page={page}').content, 'lxml')
        if len(soup.find_all('guid')) != 0:
            lis.extend(soup.find_all('guid'))
        elif len(soup.find_all('guid')) == 0:
            break
        # print(rget(f'https://{username}.artstation.com/rss').json()) 
    return lis



def download_file(url, file_path, file_name):

    file_full_path = os.path.join(file_path, file_name)
    if os.path.exists(file_full_path):
        print('[Exist][image][{}]'.format(file_full_path))
    else:
        r = rget(url)
        os.makedirs(file_path, exist_ok=True)
        with open(file_full_path, "wb") as code:
            code.write(r.content)
        print('[Finish][image][{}]'.format(file_full_path))


def download_project(hash_id):
        url = 'https://www.artstation.com/projects/{}.json'.format(hash_id)
        try:
            r = rget(url)
        except :
            time.sleep(3)
        j = r.json()
        assets = j['assets']
        title = j['slug'].strip()
        # self.log('=========={}=========='.format(title))
        username = j['user']['username']
        for asset in assets:
            assert(root_path)
            user_path = os.path.join(root_path, username)
            file_path = os.path.join(user_path, title)
            os.makedirs(user_path, exist_ok=True)
            if asset['has_image']: 
                url = asset['image_url']
                file_name = urlparse(url).path.split('/')[-1]

                try:

                    futures.append(executor.submit(download_file,
                                                             url, file_path, file_name))
                except Exception as e:
                    print(e)
            

def main():
    import argparse
    parser = argparse.ArgumentParser(
        prog='ArtStationDownloader',
        description='ArtStation Downloader is a lightweight tool to help you download images from the ArtStation')
    parser.add_argument('-u', '--username',
                        help='choose who\'s project you want to download, one or more', nargs='*')
    parser.add_argument('-f', '--file', help='input text file')
    
    args = parser.parse_args()
    print(args)

    if  args.username:
        for user in args.username:
            for i in get_projects(user):
                hash_id = str(i).replace("</guid>", '').split("/")[-1]
                # print(hash_id)
                try:
                    download_project(hash_id)
                except:
                    pass
    elif args.file:
        if os.path.exists(args.file):
            with open('art.txt','r') as f:
                for user in f.read().splitlines():
                    for i in get_projects(user):
                        print(i)
                        hash_id = str(i).replace("</guid>", '').split("/")[-1]
                        # print(hash_id)
                        try:
                            download_project(hash_id)
                        except:
                            pass

        else: 
            print(f"{args.file} DOES NOT EXIST")


main()

