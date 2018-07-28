import requests
import bs4
import os
from CConection import Conection
import json
import io
import subprocess
from subprocess import DEVNULL, STDOUT, check_call


class DownloaderSpankBang:

    def __init__(self, _output_dir, _search, _first_page, _last_page):
        self.output_dir = _output_dir
        self.search = _search
        self.first_page = _first_page
        self.last_page = _last_page
        self.i = 1
        self.j = 1
        self.Conection = Conection()
        self.list_link = []

    def download(self):
        self.list_link = self.get_list_link()
        if self.list_link != 0:
            for j in range(0, len(self.list_link)):
                self.json_details_write(len(self.list_link), j, self.list_link[j])
                command = 'youtube-dl \"' + self.list_link[j] + '\"' + ' --output \\' + self.output_dir + '\\%(title)s.%(ext)s'
                os.system(command)

    def download_hiden(self):
        self.list_link = self.get_list_link()
        if self.list_link != 0:
            for j in range(0, len(self.list_link)):
                self.json_details_write(len(self.list_link), j, self.list_link[j])
                command = 'youtube-dl \"' + self.list_link[j] + '\"' + ' --output \\' + self.output_dir + '\\%(title)s.%(ext)s'
                info = subprocess.STARTUPINFO()
                info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                info.wShowWindow = subprocess.SW_HIDE
                proc = subprocess.call(command, startupinfo=info)

    def get_list_link(self):
        self.list_link = []
        if self.Conection.get_status():
            for self.i in range(self.first_page, self.last_page):
                response = requests.get(str('https://br.spankbang.com/s/' + self.search + '/' + str(self.i)) + "/")
                soup = bs4.BeautifulSoup(response.text, "html.parser")
                for div in soup.find_all(class_='video-item'):  # video-item é a classe de div que contém os links
                    link = "https://br.spankbang.com" + str(div.find('a')['href'])
                    self.list_link.append(link)
            return self.list_link
        else:
            print("No conection... ")
            return 0

    # writing a json file to the graphic layer

    def json_details_write(self, _list_size, _current_number, _current_link):
        percent = (_current_number/_list_size)*100  # percent calc
        # Define data
        data = {'%': percent,
                'range': _list_size,
                'current': _current_number,
                'link': _current_link}
        # Write JSON file
        with io.open('data.json', 'w', encoding='utf8') as outfile:
            str_ = json.dumps(data, indent=4, sort_keys=True, separators=(',', ': '), ensure_ascii=False)
            outfile.write(str_)