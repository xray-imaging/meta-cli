import sys
import json
import pathlib


def main(args):

    if len(sys.argv) == 1:
        print ('ERROR: Must provide the path to a run-file folder as the argument')
        print ('Example:')
        print ('        python tomcat.py /nocturn/data/tomcat.json')
        sys.exit(1)
    else:

        file_name   = sys.argv[1]
        p = pathlib.Path(file_name)
        if p.is_file():
            print(file_name)  
            with open(file_name, 'r') as f:
                metadata = json.load(f)
            print(json.dumps(metadata, sort_keys=True, indent=4))

        else:
            print('ERROR: %s does not exist' % p)
            sys.exit(1)

if __name__ == "__main__":
   main(sys.argv)