import vk


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

        saved_photos = api.photos.get(album_id="saved")
        photos_urls = list()
        for photo in saved_photos:
            for key, value in photo.items():
                if (key == "src_big"):
                    photos_urls.append(value)
        print("You've got {} saved photos!".format(len(photos_urls)))
        return photos_urls

    def get_credentials(self, api):
        '''Get current user's name and last name.'''

        first_name = api.users.get()[0]["first_name"]
        last_name = api.users.get()[0]["last_name"]
        return (first_name, last_name)
