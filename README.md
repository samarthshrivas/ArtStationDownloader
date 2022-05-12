# ArtStationDownloader
This tools helps you to download images of user from ArtStation

## Download
Clone this repo 

`git clone https://github.com/samarthshrivas/ArtStationDownloader.git`

## USAGE
```
python artsunc.py -h
usage: ArtStationDownloader [-h] [-u [USERNAME ...]] [-d DIRECTORY] [-f FILE]

ArtStation Downloader is a lightweight tool to help you download images from the ArtStation

optional arguments:
  -h, --help            show this help message and exit
  -u [USERNAME ...], --username [USERNAME ...]
                        choose who's project you want to download, one or more
  -d DIRECTORY, --directory DIRECTORY
                        output directory
  -f FILE, --file FILE  input text file
```

## Download from text file file 
`python artsunc.py -f art.txt`

## Download from  multiple artist 
`python artsunc.py -u artist1 artist2`


###Used his code
[findix](https://github.com/findix/ArtStationDownloader)
