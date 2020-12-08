from holehe.core import *

def debug(DEBUG):
    if not DEBUG:
        checkVersion = httpx.get("https://pypi.org/pypi//json")
    if not DEBUG and checkVersion.json()["info"]["version"] != __version__:
        if os.name != 'nt':
            p = Popen(["pip3",
                       "install",
                       "--upgrade",
                       "git+git://github.com/megadose/@master"],
                      stdout=PIPE,
                      stderr=PIPE)
        else:
            p = Popen(["pip",
                       "install",
                       "--upgrade",
                       "git+git://github.com/megadose/@master"],
                      stdout=PIPE,
                      stderr=PIPE)
        (output, err) = p.communicate()
        p_status = p.wait()
        print(" has just been updated, you can restart it. ")
        exit()
