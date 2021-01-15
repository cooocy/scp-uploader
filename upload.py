import os
import sys
import time

# make sure that your public key was added to the host's `.ssh/authorized_keys`
# the host ip you want to upload to
host = ''
# the user name
user = ''
# the dist base dir, ends with '/'
base_dir = ''


def get_file_type(file_path):
    if file_path.endswith('jpg') or file_path.endswith('jpeg') or file_path.endswith('png') \
            or file_path.endswith('webp'):
        return 'pic'
    if file_path.endswith('md') or file_path.endswith('txt') or file_path.endswith('pages'):
        return 'document'
    if file_path.endswith('mp3'):
        return 'audio'
    if file_path.endswith('mp4') or file_path.endswith('avi') or file_path.endswith('mkv'):
        return 'video'
    if file_path.endswith('zip') or file_path.endswith('7z'):
        return 'com'
    return 'other'


def now():
    return time.strftime("%Y%m%d%H%M%S", time.localtime())


def get_file_name(file_path):
    return file_path[file_path.rindex('/') + 1:] if file_path.__contains__('/') else file_path


def gen_oss_file_name(file_path):
    return get_file_type(file_path) + '-' + now() + '-' + get_file_name(file_path)


def upload(src, dest):
    result = os.system('scp -r %s %s@%s:%s' % (src, user, host, dest))
    print('scp => src: %s, dest: %s, result: %s' % (src, dest, result))


if __name__ == '__main__':
    """
    Execute this script to scp files to dest host. e.g.
    `python3 upload_to_ecs.py /Users/ddyul/images`
    Notice that only the file not starting with '.' will be uploaded, dirs also be ignored.
    """

    argv = sys.argv
    if len(argv) != 2:
        print('error, args len must eq 2')
        exit(1)

    src_path = argv[1]
    if not src_path.endswith('/'):
        src_path += '/'

    dirs = os.listdir(src_path)
    for file in dirs:
        absolute_path = src_path + file
        # ignore dir and the file starting with '.'
        if os.path.isfile(absolute_path) and not file.startswith('.'):
            upload(absolute_path, base_dir + gen_oss_file_name(file))
