# Made by Theo Coombes, 2020
import dropbox
import json
import os

def download(path):
    global currentcount    
    for entry in dbx.files_list_folder(path, include_non_downloadable_files=False).entries:
        if "." in entry.name: # Check for files
            currentcount += 1
            newpath = download_path[:-1] + path + "/"
            os.makedirs(newpath, exist_ok=True)
            downloadto = os.path.abspath(download_path + path + "/" + entry.name)
            filedir = path + "/" + entry.name
            try:
                dbx.files_download_to_file(downloadto, filedir)
                print(f"Downloaded {entry.name}! \nCount: {currentcount}/{totalcount}")
            except dropbox.exceptions.ApiError:
                print(f"Failed to download file: {entry.name}\nReason: API Error")
        else:
            try:
                download(path + "/" + entry.name)
            except dropbox.exceptions.ApiError:
                currentcount += 1
                newpath = download_path[:-1] + path + "/"
                os.makedirs(newpath, exist_ok=True)
                downloadto = os.path.abspath(download_path + path + "/" + entry.name)
                filedir = path + "/" + entry.name
                try:
                    dbx.files_download_to_file(downloadto, filedir)
                    print(f"Downloaded {entry.name}! \nCount: {currentcount}/{totalcount}")
                except dropbox.exceptions.ApiError:
                    print(f"Failed to download file: {entry.name}\nReason: API Error")


def getFileCount(path):
    count = 0
    for entry in dbx.files_list_folder(path, include_non_downloadable_files=False).entries:
            if "." in entry.name: # Check for files
                count += 1
            else:
                try:
                    count += getFileCount(path + "/" + entry.name)
                except dropbox.exceptions.ApiError:
                    count += 1
    return count

def validate(path):
    skipped = []
    for entry in dbx.files_list_folder(path, include_non_downloadable_files=False).entries:
            if "." in entry.name: # Check for files
                if not os.path.exists(os.path.abspath(download_path + path + "/" + entry.name)):
                    skipped.append(path + "/" + entry.name)
            else:
                try:
                    skipped.extend(validate(path + "/" + entry.name))
                except dropbox.exceptions.ApiError:
                    if not os.path.exists(os.path.abspath(download_path + path + "/" + entry.name)):
                        skipped.append(path + "/" + entry.name)
    return skipped

with open("credentials.json", 'r') as f:
	settings = json.load(f)

download_path = settings["local-download-path"]
dropbox_download_dir = settings["dropbox-download-dir"]
currentcount = 0

dbx = dropbox.Dropbox(settings["access-token"])
print("Logged in.")

print("Getting total file count...")
totalcount = getFileCount(dropbox_download_dir)
print("Done.")

print("Starting downloads...")
download(dropbox_download_dir)
print("Finished downloading!")

print("Validating downloads...")
failed = validate(dropbox_download_dir)
if len(failed) != 0:
	with open("failed.txt", "w+") as f:
		f.write('\n'.join(failed))
	print(f"Done!\n{len(failed)} file(s) failed to download.")
	print("View failed.txt for a list of these files.")
else:
	print("Done!\nAll files successfully downloaded.")
