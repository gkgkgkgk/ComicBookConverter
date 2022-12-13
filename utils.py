import os
import stat

def init_video(name):
    if os.path.exists(name):
        rmtree(name)

    os.mkdir(name)
    os.mkdir(os.path.join(name,"audio"))
    os.mkdir(os.path.join(name,"frames"))
    os.mkdir(os.path.join(name,"temp"))
    os.mkdir(os.path.join(name,"speech_text"))
    os.mkdir(os.path.join(name,"matched_text"))

    return name


def rmtree(top):
    for root, dirs, files in os.walk(top, topdown=False):
        for name in files:
            filename = os.path.join(root, name)
            os.chmod(filename, stat.S_IWUSR)
            os.remove(filename)
        for name in dirs:
            rmtree(os.path.join(root, name))
    os.chmod(top, stat.S_IWUSR)
    os.rmdir(top) 