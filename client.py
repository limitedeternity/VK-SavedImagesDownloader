import math

import vk


class User(object):
    '''VK user class.'''

    def __init__(self, token):
        self.access_token = token

    def auth(self):
        '''Authorizating user with access to photos.'''

        session = vk.Session(access_token=self.access_token)
        api = vk.API(session, v='5.74')
        return api

    def get_photos(self, api):
        '''Get list of saved photos URL's.'''

        albums = api.photos.getAlbums(need_system=1)["items"]
        saved_photos = [x for x in albums if x["id"] == -15][0]
        photos_count = saved_photos["size"]

        print("You've got {} saved photos!".format(photos_count))
        photos_urls = []

        for i in range(math.ceil(photos_count / 1000)):
            saved_photos = api.photos.get(album_id="saved", count=1000, offset=i*1000)
            for photo in saved_photos["items"]:
                photo_resolutions = sorted([(key, value) for key, value in photo.items() if key.startswith("photo_")])
                photos_urls.append(photo_resolutions[-1][1])

        return photos_urls

    def get_credentials(self, api):
        '''Get current user's name and last name.'''

        first_name = api.users.get()[0]["first_name"]
        last_name = api.users.get()[0]["last_name"]
        return (first_name, last_name)
