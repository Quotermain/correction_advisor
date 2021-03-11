import pickle
from sys import argv

def load_pickle_object(file_path):
    with open(file_path, 'rb') as file:
        object = pickle.load(file)
    return object

if __name__ == '__main__':
    file_path = argv[1]
    print(load_pickle_object(file_path))
