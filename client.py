import vk
import math


class User(object):
    '''VK user class.'''

    def __init__(self, token):
        self.access_token = token

    def auth(self):
        '''Authorizating user with access to photos.'''

        session = vk.Session(access_token=self.access_token)
        api = vk.API(session)
        return api

    def get_photos(self, api):
        '''Get list of saved photos URL's.'''

        photos_count = api.photos.getAlbums(album_ids=-15)[0]['size']
        photos_urls = []

        for i in range(math.ceil(photos_count / 1000)):
            saved_photos = api.photos.get(album_id="saved", count=1000, offset=i*1000)
            for photo in saved_photos:
                photos_urls.append(photo["src_big"])

        print("You've got {} saved photos!".format(photos_count))
        return photos_urls

    def get_credentials(self, api):
        '''Get current user's name and last name.'''

        first_name = api.users.get()[0]["first_name"]
        last_name = api.users.get()[0]["last_name"]
        return (first_name, last_name)
