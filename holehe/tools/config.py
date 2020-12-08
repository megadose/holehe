from holehe.core import *

def import_submodules(package, recursive=True):
    """Get all the  submodules"""
    if isinstance(package, str):
        package = importlib.import_module(package)
    results = {}
    for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
        full_name = package.__name__ + '.' + name
        results[full_name] = importlib.import_module(full_name)
        if recursive and is_pkg:
            results.update(import_submodules(full_name))
    return results


def get_functions(modules):
    """Transform the modules objects to functions"""
    websites = []
    for module in modules:
        if len(module.split(".")) > 2:
            modu = modules[module]
            site = module.split(".")[-1]
            websites.append(modu.__dict__[site])
    return websites

def check_email(email):
    """ Check if the string is a valid email"""
    if len(email) < 5 or '@' not in email:
        return
    suffix = email.split('@')[1]
    print(suffix)
    if '.' not in suffix:
        return
    if len(suffix.split('.')[0]) < 1:
        return
    else:
        return email

def ask_email():
    """ Check if the user pass an argument. Returns the email adress if valids."""
    if len(sys.argv) < 2:
        exit("[-] Please enter a target email ! \nExample :  email@example.com")
    else:
        email = sys.argv[1]
    if not (check_email(email)):
        exit("[-] Please enter a target email ! \nExample :  email@example.com")
    return email
