import json
import os
from collections import OrderedDict
from itertools import groupby
from shutil import copyfile

from dateutil import parser


def render(source, target, context = "None"):
    items = _load_items(source)

    msg = dict()

    for k in items:
        id = k['message_id']
        msg[id] = k

    items = list(msg.values())
    items.sort(key=lambda x: x['_time'])

    os.makedirs(target, exist_ok=True)

    index_file = os.path.join(target, 'index.html')

    with open(index_file, mode='w', encoding='utf-8') as w:
        w.write('<!DOCTYPE html>\n<html lang="en">\n')
        w.write('<head>\n')
        w.write('<meta charset="utf-8">\n')
        w.write('<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">\n')

        w.write('<link rel="stylesheet" type="text/css" href="/style.css">\n')
        w.write(
            '<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/css/bootstrap.min.css" integrity="sha384-GJzZqFGwb1QTTN6wy59ffF1BuGJpLSa9DkKMp0DgiMDm4iYMj70gZWKYbI706tWS" crossorigin="anonymous">\n')
        w.write('</head>')
        w.write('<body>')

        w.write('<div class="container">')
        w.write('<h1>{0}</h1>\n'.format(context))

        for k, g in groupby(items, lambda x: x['_date']):

            w.write('<h2>{0}</h2>\n'.format(k))
            for i in g:
                w.write('<div class="row"><div class="col-12 justify-content-center col-md-8">\n')

                text = i.get('text', None)
                if text:
                    lines = text.split('\n')

                    w.write('<p>' + '<br>\n'.join(lines) + '</p>\n')

                if 'video' in i:
                    video = i['video']
                    video_name = copy_to_target(video, target)
                    thumb_name = copy_to_target(video['thumb'], target)


                    w.write("<video controls poster='{2}' preload='none'>"
                            "<source src='{0}' type='{1}'></video>\n".format(video_name, video['mime_type'], thumb_name))

                photos = i.get('photo', None)
                if photos:
                    photo = None

                    # pick first sha1
                    for p in photos:

                        if 'sha1' in p:
                            photo = p
                            break
                    name = copy_to_target(photo, target)


                    w.write("<img src='{0}' class='img-fluid'>\n".format(name))
                w.write('</div></div>')  # row

        w.write('</div>\n')
        w.write('</body></html>')
    print('rendered')

def copy_to_target(file, target):
    name = file.get('name', None) or os.path.basename(file['file_path'])

    dest_file = os.path.join(target, name)
    if not os.path.exists(dest_file):
        copyfile(file['sha1'], dest_file)

    return name


def _load_items(dir):
    name = os.path.join(dir, 'index.json')

    if not os.path.isfile(name):
        return []

    items = []

    # unique = set()
    with open(name, mode='r') as js:
        for line in js:
            if line:
                # if line in unique:
                #    continue
                # unique.add(line)

                item = json.loads(line)

                d = parser.parse(item['_time'])

                item['_time'] = d
                item['_date'] = d.date()

                items.append(item)
    return items