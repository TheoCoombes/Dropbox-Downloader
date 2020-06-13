# Dropbox Downloader
A simple script to download files from dropbox

## **Requirements**


- `pip install dropbox`
- Python >= 3.7 (Written in Python 3.8.2)

## **How to setup:**

- Create an app in the [App Console](https://www.dropbox.com/developers/apps)
- Set permission type to *"Full Dropbox"*
- Generate an access token by scrolling down on the app's page and pressing generate on the OAuth 2 section (see image)
- Paste the access token into the settings.json file
- Configure *"local-download-path"* on settings.json to the directory you want your files to download to.
- Configure *"dropbox-download-dir"* on settings.json to the directory on dropbox you want your files downloaded from (Leave at "" for all files).



## **Custom Downloads**
You can also call the `download(dropbox_path)` function to download a file at a certain dropbox location.
Just remember to globally set a `download_path` first or be prepared for a bunch of errors :)
