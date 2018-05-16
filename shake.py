import attr
import json
import re
import xml.etree.ElementTree as ElementTree
from typing import List

@attr.s
class Intro:
    text : str

@attr.s
class Act:
    text : str

@attr.s
class Play:
    intro : Intro
    acts : List[Act]


def apply_filters(filters, data):
    current = data
    for f in filters:
        current = f(current)
    return current

def remove_tab_char(data):
    return data.replace('\t', ' ')

def replace_tab_tags(data):
    return data.replace('<tab>', '\t')

def remove_page_breaks(data):
    return re.sub(r'</poem>\n+<poem>', '\n ', data)

def enclose_in_xml_tag(data, tag):
    return f'<{tag}>{data}</{tag}>'

def parse_xml(data):
    tree = ElementTree.fromstring(data)
    return tree

def find_parts(data):
    parts = list(data)
    intro, *scenes = parts
    return dict(
        intro=intro,
        scenes=scenes
        )

def transform_scene(scene):
    newlines = scene.text
    heading = scene[0]

    assert re.match(r'\n+', newlines), newlines
    assert heading.tag in ('h1', 'h2'), heading

    scene_text = ''.join(scene.itertext())
    the_start = newlines + heading.text
    assert scene_text.startswith(the_start), scene_text[0:100]
    scene_text = scene_text[len(the_start):]

    scene = re.match(r'\n+(.+?)\n\n(.+)', scene_text, flags=re.DOTALL)
    scene = {
        'heading': heading,
        'location': scene.group(1),
        'text': scene.group(2)
        }

    return scene

def parse_scenes(data):
    data['scenes'] = [transform_scene(s) for s in data['scenes']]
    return data


def split_acts(data):
    acts = []

    for scene in data['scenes']:

        heading = scene['heading']
        if heading.tag == 'h1':
            act = {
                'heading': heading.text,
                'scenes': []
            }
            acts.append(act)

        scene['heading'] = heading.text
        act['scenes'].append(scene)

    del data['scenes']
    data['acts'] = acts
    return data





filters = [
    remove_tab_char,
    replace_tab_tags,
    remove_page_breaks,
    lambda d: enclose_in_xml_tag(d, 'book'),
    parse_xml,
    find_parts,
    parse_scenes,
    split_acts,
]

if __name__ == '__main__':
    with open('data/Hamlet/svensk.txt') as f:
        data = f.read()

    result = apply_filters(filters, data)
    print(result)

    # with open('out.json', 'w') as f:
    #     print(result, file=f)
        # json.dump(result, f)
