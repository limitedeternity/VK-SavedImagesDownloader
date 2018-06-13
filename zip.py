from os import path, listdir
import zipfile


def zip_contents(folder):
    zip_list = []
    chunks = []

    for entry in listdir(folder):
        if path.isfile(path.join(folder, entry)):
            zip_list.append(entry)

    for item in range(0, len(zip_list), 1000):
        chunks.append(zip_list[item:item + 1000])

    for index, chunk in enumerate(chunks):
        with zipfile.ZipFile(folder + '-' + str(index) + '.zip', 'w', zipfile.ZIP_DEFLATED) as zip:
            for file in chunk:
                zip.write(path.join(folder, file), file)
