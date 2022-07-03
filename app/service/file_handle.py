# Read csv file to map
import pickle


def read_csv_file(file):
    map = {}
    with open(file) as file:
        for line in file:
            list_params = line.split(",")
            nft_id = str(list_params[0]).strip()
            nft_img_path = str(list_params[1]).strip()
            map[nft_img_path] = nft_id
    return map


def read_pkl_file(_path):
    data = None
    with open(_path, "rb") as f:
        data = pickle.load(f)
    return data


def append_data_2_pkl_file(data, path):
    with open(path, "ab+") as input_file:
        pickle.dump(data, input_file)


def load_pickle_file(path):
    res = list()
    try:
        res.extend(pickle.load(open(path, "rb")))
    except EOFError:
        pass
    return res
