def read(path):
    with open(path, 'r') as file:
        return file.read()
def write(path, text):
    with open(path, 'w') as file:
        file.write(text)