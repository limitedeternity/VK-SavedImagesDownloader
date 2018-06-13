import functools
import os
import shutil
import sys
import time
import webbrowser
from multiprocessing import Pool

import requests

from client import User
from zip import zip_contents


def create_folder(credentials):
    '''Create a folder to store photos named after your VK
    first and last name.'''

    folder_name = "_".join(credentials)

    if not os.path.exists(folder_name):
        os.makedirs(folder_name, exist_ok=True)

    print("Directory {} is created!".format(folder_name))
    return folder_name


def photos_downloader(url, folder_name):
    '''Download all the photos into folder_name'''

    file_name = str(url.split("/")[-1])
    s = requests.Session()
    r = s.get(url, stream=True)

    if r.status_code == 200:
        with open(os.path.join(folder_name, file_name), "wb") as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
            print("{} downloaded.".format(file_name))

    else:
        print("{} skipped.".format(file_name))


if __name__ == '__main__':
    webbrowser.open_new_tab('https://oauth.vk.com/authorize?client_id=6449285&response_type=token&scope=84&redirect_uri=https://limitedeternity.github.io/VK-SavedImagesDownloader/')

    try:
        access_token = input("Place access token here: ")
        user = User(token=access_token)
        vk_api = user.auth()
        print("Authorization successful.")

    except Exception:
        print("Your input data seems to be wrong. Please try again!")
        sys.exit(1)

    except KeyboardInterrupt:
        print("Keyboard interrupt detected!")
        sys.exit(0)

    try:
        start_time = time.time()
        creds = user.get_credentials(vk_api)
        folder = create_folder(creds)
        urls = user.get_photos(vk_api)

        p = Pool()
        p.map(functools.partial(photos_downloader, folder_name=folder), urls)
        p.close()
        p.join()

    except Exception as e:
        print(e)
        sys.exit(1)

    except KeyboardInterrupt:
        print("Keyboard interrupt detected!")
        sys.exit(0)

    finally:
        print("Zipping folder...")
        zip_contents(folder)
        shutil.rmtree(folder)

        print("--- Done in {0:.2f} seconds ---".format(time.time() - start_time))
