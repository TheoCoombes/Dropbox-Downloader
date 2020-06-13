# Made by Theo Coombes, 2020
import dropbox
import json
import os

def download(path):
    for entry in dbx.files_list_folder(path, include_non_downloadable_files=False).entries:
            if "." in entry.name: # Check for files
                newpath = download_path[:-1] + path + "/"
                os.makedirs(newpath, exist_ok=True)
                downloadto = os.path.abspath(download_path + path + "/" + entry.name)
                filedir = path + "/" + entry.name
                try:
                    dbx.files_download_to_file(downloadto, filedir)
                except dropbox.exceptions.ApiError:
                    print(f"Failed to download file: {entry.name}")
            else:
                download(path + "/" + entry.name)

with open("credentials.json", 'r') as f:
	settings = json.load(f)

download_path = settings["local-download-path"]
dropbox_download_dir = settings["dropbox-download-dir"]

dbx = dropbox.Dropbox(settings["access-token"])
print("Logged in.")


print("Starting downloads...")
download(dropbox_download_dir)
print("Finished downloading!")
