import os
from ftplib import FTP, FTP_TLS
import logging

HOST_URL = os.environ.get('HOST_URL', 'localhost')
USERNAME = os.environ.get('USERNAME', 'bob')
PASSWORD = os.environ.get('PASSWORD', 'secret')
WORKDIR = os.environ.get('WORKDIR', 'ohh/look/this')
SOURCEDIR = os.environ.get('SOURCEDIR', './test/sourcedir')


# Set logger
FORMAT = '[%(asctime)-15s]  %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def upload_ftp ():
    # FTP Connect
    logger.info('Connecting')
    ftp = FTP_TLS(HOST_URL)

    ftp.login(USERNAME, PASSWORD)
    ftp.prot_p()

    # Validate connection
    ftp.retrlines('LIST')
    
    logger.info('Connected')
    files = ftp.nlst()

    # Go to WORKDIR to start the uploading.
    directory_tree = WORKDIR.split('/')
    for directory in directory_tree:
        files = ftp.nlst()
        print(files)
        if not directory in files:
            ftp.mkd(directory)
        ftp.cwd(directory)

    # Scan local direcotry
    logger.info('scanning')
    srcdir_length = len(SOURCEDIR)  # To extract the root path from the workir
    # Upload process.
    for root, dirs, files in os.walk(SOURCEDIR, topdown=True):
        # Getting work directory
        logger.info('ROOT: {}'.format(root))
        cwd = root[srcdir_length:]
        cwd = str.replace(cwd, '\\', '/')   # Windows directory structure.
        workdir ='/{}{}'.format(WORKDIR, cwd)
        # Go the new wordir to start uploading.
        ftp.cwd(workdir)
        logger.debug('remote pwd: {}'.format(ftp.pwd()))

        for file_name in files:
            # Avoid Unix hidden files.
            if file_name[0] == '.':
                continue

            file_path = os.path.join(root, file_name)
            logger.info('FILE: {}, PATH: {}'.format(file_name, file_path))
            # Store file.
            store_cmd = 'STOR ./{}'.format(file_name)
            with open(file_path, 'rb') as f:
                print(store_cmd)
                ftp.storbinary(store_cmd, f)

        for dir_name in dirs:
            file_path = os.path.join(root, dir_name)
            logger.info('DIR: {}, PATH: {}'.format(dir_name, file_path))
            # Create folder if does not exists.
            files = ftp.nlst()
            if not (dir_name in files):
                ftp.mkd(dir_name)

    logger.info('Finished upload.')
    ftp.quit()



if __name__ == '__main__':
    upload_ftp()
