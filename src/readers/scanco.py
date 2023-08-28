import sys
import itk
import json
import pathlib


def jsonify(data):
    json_data = dict()
    for key, value in data.items():
        if isinstance(value, list): # for lists
            value = [ jsonify(item) if isinstance(item, dict) else item for item in value ]
        if isinstance(value, dict): # for nested lists
            value = jsonify(value)
        if isinstance(key, int): # if key is integer: > to string
            key = str(key)
        if type(value).__module__=='numpy': # if value is numpy.*: > to python list
            value = value.tolist()
        json_data[key] = value
    return json_data


def main(args):

    if len(sys.argv) == 1:
        print ('ERROR: Must provide the path to a run-file folder as the argument')
        print ('Example:')
        print ('        python scanco.py /Users/decarlo/conda/nocturn/data/FEG230530_413/')
        sys.exit(1)
    else:

        file_name   = sys.argv[1]
        p = pathlib.Path(file_name)
        if p.is_file():
            image = itk.imread(file_name)   
            metadata = dict(image)
            print(json.dumps(jsonify(metadata), sort_keys=True, indent=4))

        else:
            print('ERROR: %s does not exist' % p)
            sys.exit(1)

if __name__ == "__main__":
   main(sys.argv)