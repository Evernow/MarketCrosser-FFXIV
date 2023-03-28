import gzip
import shutil
from datetime import datetime
from ftplib import FTP
import io
import glob
import os
import traceback
import multiprocessing
import time
import tarfile
parent_directory = r""
# Download files from VPS FTP server
start = datetime.now()
ftp = FTP('65.108.202.158')
ftp.login('wistful','#GUbNyA4yMj4PY@m')
ftp.cwd('PersonalPlayGround')
files = ftp.nlst()
ftp.retrbinary("RETR " + 'compressFileName.tar.gz' ,open(os.path.join(parent_directory, 'compressFileName.tar.gz'), 'wb').write,102400)
# ("RETR " + file ,open(os.path.join(parent_directory, file), 'wb').write,102400)
ftp.close()
# Uncompress said files
file = tarfile.open(os.path.join(parent_directory,'compressFileName.tar.gz'))
file.extractall(parent_directory)
file.close()
print('Done')