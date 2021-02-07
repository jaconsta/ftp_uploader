import os
from ftplib import FTP_TLS
import logging

HOST_URL = os.environ.get('HOST_URL', 'localhost')
USERNAME = os.environ.get('USERNAME', 'bob')
PASSWORD = os.environ.get('PASSWORD', 'secret')
REMOTE_WORKDIR = os.environ.get('WORKDIR', 'ohh/look/this')
SOURCEDIR = os.environ.get('SOURCEDIR', './test/sourcedir')


# Set logger
FORMAT = '[%(asctime)-15s]  %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def ftp_connect(func):
    def wrapper():
        logger.info('Connecting')
        ftp = FTP_TLS(HOST_URL, user=USERNAME, passwd=PASSWORD)
        logger.info('Connected')

        logger.info(ftp.getwelcome())
        logger.info('...')
        logger.info('..')
        logger.info('.')

        func(ftp)

        logger.info('Gracefully closing FTP.')
        ftp.quit()

    return wrapper


def concat_file_path(directory: str, name: str) -> str:
    return os.path.join(directory, name)


def is_hidden_file(filename: str) -> bool:
    return filename.startswith('.')


def scan_local_content():
    logger.info('scanning local')
    for root, dirs, files in os.walk(SOURCEDIR, topdown=True):
        for file_name in files:
            if is_hidden_file(file_name):
                continue
            yield root, file_name, True

        for dir_name in dirs:
            yield root, dir_name, False


def get_work_dir(new_path: str) -> str:
    srcdir_length = len(SOURCEDIR) + 1
    cwd = new_path[srcdir_length:]
    cwd = str.replace(cwd, '\\', '/')   # Windows directory structure.
    workdir = os.path.join('/', REMOTE_WORKDIR, cwd)
    return workdir


def handle_update(ftp: FTP_TLS):
    remote_cwd = ''
    files_in_remote_cwd = []

    def load_remote_dir(current_working_directory: str) -> None:
        should_load_directory = False
        current_cwd = get_work_dir(current_working_directory)
        nonlocal remote_cwd
        nonlocal files_in_remote_cwd

        if remote_cwd != current_cwd:
            remote_cwd = current_cwd
            should_load_directory = True

        if should_load_directory:
            # logger.info(f'changin directory {remote_cwd}')
            ftp.cwd(remote_cwd)
            files_in_remote_cwd = ftp.nlst()

    load_remote_dir(SOURCEDIR)
    logger.info(f'Initial folder {remote_cwd}')

    def call(file_folder: str, filename: str, is_file: bool):
        load_remote_dir(file_folder)

        if is_file:
            file_path = concat_file_path(file_folder, filename)
            store_cmd = 'STOR ./{}'.format(filename)
            with open(file_path, 'rb') as f:
                logger.info(f'STOR {remote_cwd} {filename}')
                ftp.storbinary(store_cmd, f)
        else:
            if not (filename in files_in_remote_cwd):
                logger.info(f'New folder {concat_file_path(file_folder, filename)}')
                ftp.mkd(filename)

    return call


@ftp_connect
def list_and_update_content(ftp: FTP_TLS):
    update_manager = handle_update(ftp)
    for remote_list in scan_local_content():
        update_manager(*remote_list)


def main() -> None:
    list_and_update_content()


if __name__ == '__main__':
    main()
