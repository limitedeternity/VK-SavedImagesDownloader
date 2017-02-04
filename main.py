import vk
import urllib.request
from multiprocessing import Pool
import os
import getpass
import time

start_time = time.time()


def login(app_id='5606767'):
    '''Login and initiate VK session.'''

    login = str(input("Enter your login: "))
    password = str(getpass.getpass("Enter your password: "))
    session = vk.AuthSession(app_id, login, password, scope='photos')
    return vk.API(session)


def get_saved_photos():
    '''Get all of the source links for photos in "Saved" album.'''

    saved_photos = vk_api.photos.get(album_id='saved')

    photos_urls = []
    for photo in saved_photos:
        for key, value in photo.items():
            if (key == 'src_big'):
                photos_urls.append(value)
    print("You've got {} saved photos!".format(len(photos_urls)))
    return photos_urls


def make_folder():
    '''Create a folder called after your first and last name'''

    folder_name = vk_api.users.get()[0]['first_name'] +\
        "_" + vk_api.users.get()[0]['last_name']
    if not os.path.exists(folder_name):
        os.makedirs(folder_name, exist_ok=True)
    print("Directory {} is already created!".format(folder_name))
    return str(folder_name)


def photos_downloader(url):
    '''Download all the photos in newly-created directory
     named after your VK credentials.'''

    file_name = str(url.split('/')[-1])
    u = urllib.request.urlopen(url)
    with open(os.path.join(folder_name, file_name), 'wb') as f:
        f.write(u.read())
        print("{} downloaded.".format(file_name))


if __name__ == '__main__':

    try:
        vk_api = login()
    except vk.exceptions.VkAuthError as e:
        print(e)
    else:
        folder_name = make_folder()
        p = Pool()
        urls = [image for image in get_saved_photos()]
        p.map(photos_downloader, urls)
    finally:
        print("---Done in %s seconds ---" % (time.time() - start_time))
