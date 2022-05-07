# Zip All
This app (no GUI, this is a CLI app) will zip files of a folder. It will give the archives the '.cbz' extension. This app is useful to turn a large amount of images into formats readable by comic or manga readers such as CDisplayEx. It can easily be modified to keep the archives in the ".zip" format instead of creating ".cbz" archives. Additionally, this script will also sort the files by creation date (in other words, the files of archive1 will be older than those in archive2, etc.). Again, this behavior can easily be changed so that the files are instead sorted by name, size, etc.
## Usage
CLI Argument | Short | Description |
--- | --- | --- | 
--source | -src | The directory (absolute path) where to find the files. The files are sorted by creation date. Default value: current working directory|
--destination | -dst | The directory (absolute path) where to put the compressed folders. Default value: current working directory |
--size | -s | The number of files to put in each archive. Must be greater than 0. If the number of files in the source folder is not a multiple of the size, the remaining files will be left out. Default value: 50 |
