from os import environ
from ftplib import FTP, FTP_TLS
import logging

HOST_URL = environ.get('HOST_URL', 'ftp.client.com')
USERNAME = environ.get('USERNAME', 'ftp@client.com')
PASSWORD = environ.get('PASSWORD', 'aStrongPassword')
WORKDIR = environ.get('WORKDIR', './')
HOMEDIR = environ.get('HOMEDIR', './')


# Set logger
FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
logging.basicConfig(format=FORMAT)
d = {'clientip': '192.168.0.1', 'user': 'fbloggs'}
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def upload_ftp ():
    print(HOST_URL, USERNAME, PASSWORD)
    # logging.info('Connecting')
    ftp = FTP_TLS(HOST_URL)

    # logging.debug('{0}, {1}'.format(USERNAME, PASSWORD))
    ftp.login(USERNAME, PASSWORD)
    # ftp.prot_p()

    ftp.retrlines('LIST')
    
    files = ftp.nlst()


    print ('content_web in? {is_it}'.format(is_it='content_web' in files))


    ftp.cwd('content_web')
    dir_list = ftp.nlst()
    print(dir_list)

    files = ftp.nlst()
    for f in files:
        print(f)

    # on exit
    ftp.quit()



if __name__ == '__main__':
    upload_ftp()
