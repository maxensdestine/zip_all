import os
import shutil
import argparse


def folder_format_validator(temp: str) -> str:
    if os.path.isdir(temp) and os.path.isabs(temp):
        return temp
    else:
        raise argparse.ArgumentTypeError("Not a folder or not an absolute path")



def integer_format_validator(temp: str) -> int:
    msg = "Must an integer be greater than 0"
    try:
        someVal = int(temp)
        if not someVal > 0:
            raise argparse.ArgumentTypeError(msg)
        else:
            return someVal
    except:
        raise argparse.ArgumentTypeError(msg)



def parse_arguments():
    cwd = os.getcwd()
    parser = argparse.ArgumentParser(description="This app will zip files of a folder. It will give the archives the '.cbz' extension. This app is useful to turn a large amount of images into formats readable by comic or manga readers such as CDisplayEx.")
    
    parser.add_argument("-src", "--source", type=folder_format_validator, default=cwd, help="The directory (absolute path) where to find the files. If not used, the directory of the script will be used. The files are sorted by creation date.")

    parser.add_argument("-dst", "--destination", type=folder_format_validator, default=cwd, help="The directory (absolute path) where to put the compressed folders. If not used, the directory of the script will be used")

    parser.add_argument("-s", "--size", type=integer_format_validator, default= 50, help="The number of files to put in each archive. Must be greater than 0. If the number of files in the source folder is not a multiple of the size, the remaining files will be left out. Default value: 50")

    args = parser.parse_args()

    return args.source, args.destination, args.size




def find_unique_name(safe_title: str, folder: str, index: int) -> str:
    file_name = safe_title + str(index)
    archive_name = safe_title + str(index) + ".zip"
    cbz_name = safe_title + str(index) + ".cbz"

    while os.path.exists(os.path.join(folder, file_name)) or os.path.exists(os.path.join(folder, archive_name)) or os.path.exists(os.path.join(folder, cbz_name)):
        index += 1
        file_name = safe_title + str(index)
        archive_name = safe_title + str(index) + ".zip"
        # no need to check for cbz if you only keep the zip files
        cbz_name = safe_title + str(index) + ".cbz"
    return os.path.join(folder, file_name), index + 1


def creat_archive(subdir_name: str, dst_abs: str):
    """Creates an archive from directory subdir_name inside the directory dst_abs"""
    archive = shutil.make_archive(subdir_name, "zip", subdir_name)

    #comment the 3 below lines to keep the archive as a zip file
    oldname = os.path.join(subdir_name, archive)
    newname = os.path.join(dst_abs, archive.strip("zip") + "cbz")
    shutil.move(oldname, newname)

    # only if everything was successful, do we delete the folder which contains the images
    shutil.rmtree(subdir_name)


def move_files(src_abs: str, dst_abs: str, size: int):
    """Move files into subdirectories and zip the subdirectories"""

    files = [os.path.join(src_abs, f) for f in os.listdir(src_abs)]
    
    # sort by creation time
    files.sort(key=os.path.getctime)
    # uncomment this line and comment the previous one to sort by name
    # files.sort()
    subdir_name = None
    i = 0
    index = 1
    nbfiles = len(files)
    total = nbfiles//size
    curarchive = 1

    # we add 1 so that we loop an extra time, which guarantees that the last archive will be zipped (it wouldn't if nbfiles % size == 0)
    for i in range(0, nbfiles + 1):
        # create new subdir if necessary, zip old dir if it exists
        if i % size == 0:
            if isinstance(subdir_name, str):
                creat_archive(subdir_name, dst_abs)
                curarchive = (i+1)//size
                print("Zipping... " + str(curarchive) + "/" + str(total), end="\r")
            
            if len(files) - i < size:
                # not enough files to create a full archive so we stop
                break

            subdir_name, index = find_unique_name("archive", dst_abs, index)
            os.mkdir(subdir_name)

        f = files[i]
        # move file to current dir
        f_base = os.path.basename(f)
        shutil.move(f, os.path.join(subdir_name, f_base))

    # permanent print to not make the CLI ugly
    print("Zipping... " + str(curarchive) + "/" + str(total))



def main():
    src, dst, size = parse_arguments()
    move_files(src, dst, size)


if __name__ == "__main__":
    main()
