from meta import log


def add_header(label):

    header = add_decorator(label) + '\n' + label + '\n' + add_decorator(label) + '\n\n'

    return header

def add_title(label):

    title = label + '\n' + add_decorator(label, decorator='-') + '\n\n' 

    return title


def add_decorator(label, decorator='='):
    
    return decorator.replace(decorator, decorator*len(label))