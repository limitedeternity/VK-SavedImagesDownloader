from client import User
from multiprocessing import Pool
import os
import requests
import shutil
import functools
import webbrowser
import time


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


if __name__ == '__main__':
    webbrowser.open_new_tab('https://oauth.vk.com/authorize?client_id=6044739&redirect_uri=https://oauth.vk.com/blank.html&response_type=token&scope=84')
    access_token = input("Token: ")
    try:
        user = User(token=access_token)
        vk_api = user.auth()
        print("Authorization successful.")
    except Exception:
        print("Your input data seems to be wrong. Please try again!")
    else:
        try:
            creds = user.get_credentials(vk_api)
            folder = create_folder(creds)

            p = Pool()
            urls = [image for image in user.get_photos(vk_api)]
            start_time = time.time()
            p.map(functools.partial(photos_downloader,
                                    folder_name=folder), urls)
        except Exception as e:
            print(e)
        except KeyboardInterrupt:
            print("Keyboard interrupt detected!")
        finally:
            print("---Done in {} seconds ---".format(time.time() - start_time))
