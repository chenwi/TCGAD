# coding:utf-8
# author: chenwi
# date:2018/7/12
# work code

import os
import gzip
import requests
from requests.exceptions import RequestException
from PyQt5.QtCore import QThread, pyqtSignal

requests.packages.urllib3.disable_warnings()


class WorkThread(QThread):
    signal1 = pyqtSignal([int])
    signal2 = pyqtSignal([int])
    signal3 = pyqtSignal(list)
    signal4 = pyqtSignal([int])

    def __init__(self, fileName, directory):
        super(WorkThread, self).__init__()

        self.fileName = fileName
        self.directory = directory

        self.link = r'https://api.gdc.cancer.gov/data/'

    def run(self):

        try:
            UUID_list = self.get_UUID_list()
            last_UUID = self.get_last_UUID()
            self.last_UUID_index = self.get_lastUUID_index(UUID_list, last_UUID)
            temp = self.last_UUID_index

            length = len(UUID_list)

            for UUID in UUID_list[self.last_UUID_index:]:
                url = os.path.join(self.link, UUID)
                file_path = os.path.join(self.directory, UUID)

                if self.download(url, file_path):  # download true
                    # print(temp)

                    temp += 1
                    per = 100 * temp / length
                    self.signal1.emit(per)
                    self.signal3.emit([temp, length])
                else:  # False
                    self.signal4.emit(-1)  # 404 page because of file error is  -1



        except RequestException:  # request exception from download
            self.signal2.emit(404)
        except:
            self.signal1.emit(-1)

    def download(self, url, file_path):

        r = requests.get(url, stream=True, verify=False)

        if r.status_code != 404:  # error page

            total_size = int(r.headers['content-length'])
            disposition = r.headers['Content-Disposition']
            prifile_type = disposition.split('.')[-1]
            prifile = f"{file_path}.{prifile_type}"

            temp_size = 0
            with open(prifile, "wb") as f:

                for chunk in r.iter_content(chunk_size=256):
                    if chunk:
                        temp_size += len(chunk)
                        per = 100 * temp_size / total_size
                        self.signal2.emit(per)
                        f.write(chunk)
                        f.flush()
            if prifile_type == 'gz':
                file_type = disposition.split('.')[-2]
                file = f"{file_path}.{file_type}"
                with gzip.GzipFile(prifile) as g:
                    with open(file, "wb") as f:
                        f.write(g.read())
                os.remove(prifile)
            return True
        else:
            return False  # file error

    def get_UUID_list(self):
        with open(self.fileName, 'r') as f:
            data = f.readlines()
        UUID_list = []
        for sent in data:
            UUID_list.append(sent.split('\t')[0])

        return UUID_list[1:]

    def get_last_UUID(self):
        dir_list = os.listdir(self.directory)
        if not dir_list:
            return
        else:
            dir_list = sorted(dir_list, key=lambda x: os.path.getmtime(os.path.join(self.directory, x)))
            last_UUID = dir_list[-1].split('.')
            last_UUID = ''.join(last_UUID[:-1])
            return last_UUID

    def get_lastUUID_index(self, UUID_list, last_UUID):
        for i, UUID in enumerate(UUID_list):
            if UUID == last_UUID:
                return i
        return 0
