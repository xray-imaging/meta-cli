import sys
import pprint
import xmltodict
import configparser
import pathlib

def extract_meta_from_config(file_name):
    meta_dict = {}
    # Exact meta data from config file
    try:
        with open(file_name, encoding='latin-1') as f:
            config = configparser.ConfigParser(interpolation=None)
            config.read_file(f)   

        sections = config.sections()
        meta_dict = {i: {i[0]: i[1] for i in config.items(i)} for i in config.sections()}
        # for key in meta_dict:
        #     print(key, meta_dict[key])
    except FileNotFoundError:
        print("ERROR: %s is missing." % file_name)
        exit()
    print('***********************')
    print(file_name)
    pprint.pprint(meta_dict)
    return meta_dict

def extract_meta_from_xml(file_name):
    # Extract meta data from dtxml file
    with open(file_name, encoding='latin-1') as f:
        xml_content= f.read()

    xml_dict = xmltodict.parse(xml_content)
    print('***********************')
    print(file_name)
    pprint.pprint(xml_dict)
    return xml_dict

def main(args):

    if len(sys.argv) == 1:
        print ('ERROR: Must provide the path to a run-file folder as the argument')
        print ('Example:')
        print ('        python nikon.py /data/sample_name/')
        sys.exit(1)
    else:

        file_name   = sys.argv[1]
        p = pathlib.Path(file_name)
        if p.is_dir():
            p = pathlib.Path(file_name) #.joinpath(p.stem)
            list_parts = list(p.parts)
            fname = list_parts[-1][:-22]
            list_parts.append(fname)
            p = p.joinpath(*list_parts)

            file_name_ctinfo_xml = p.with_suffix('.ctinfo.xml')
            file_name_ctprofile_xml = p.with_suffix('.ctprofile.xml')
            file_name_xtekct = p.with_suffix('.xtekct')
        else:
            print('ERROR: %s does not exist' % p)
            sys.exit(1)
    my_xtekct_dict        = extract_meta_from_config(file_name_xtekct)
    my_ctinfo_xml_dict    = extract_meta_from_xml(file_name_ctinfo_xml)
    my_ctprofile_xml_dict = extract_meta_from_xml(file_name_ctprofile_xml)

if __name__ == "__main__":
   main(sys.argv)