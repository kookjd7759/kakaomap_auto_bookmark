import os
import bookmark
setting_path = os.getcwd() + '\\kakaomap_auto_bookmark\\src\\setting.txt'
def read(path):
    with open(path, 'r') as file:
        return file.read()
def write(path, text):
    with open(path, 'w') as file:
        file.write(text)
def read_color():
    data = read(setting_path)
    return int(data[0])
def read_group():
    data = read(setting_path)
    return int(data[1])
def write_color(color):
    write(setting_path, str(color) + read(setting_path)[1:])
def write_group(group):
    write(setting_path, read(setting_path)[:1] + str(group))