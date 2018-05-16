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

def split_acts(data):
    acts = []
    for scene in data['scenes']:
        newlines = scene.text
        heading = scene[0]

        assert re.match(r'\n+', newlines), newlines
        assert heading.tag in ('h1', 'h2'), heading

        scene_text = ''.join(scene.itertext())
        the_start = newlines + heading.text
        assert scene_text.startswith(the_start), scene_text[0:100]
        scene_text = scene_text[len(the_start):]

        if heading.tag == 'h1':
            act = {
                'heading': heading.text,
                'scenes': []
            }
            acts.append(act)

        scene = {'heading': heading.text, 'text': scene_text}
        act['scenes'].append(scene)

    return acts




filters = [
    remove_tab_char,
    replace_tab_tags,
    lambda d: enclose_in_xml_tag(d, 'book'),
    parse_xml,
    find_parts,
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
