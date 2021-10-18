from src.utils.dataloader import *
from os import listdir
from os.path import join, isfile

if __name__ == '__main__':
    files = [f for f in listdir(data_path) if isfile(join(data_path, f))]
    for file in files:
        print(f'Trabajando con archivo : {file}')
        truncateTable('VENTAS_AL')
        loadFile('VENTAS_AL',file)