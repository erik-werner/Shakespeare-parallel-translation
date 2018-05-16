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

def find_intro_and_scenes(data):
    parts = list(data)
    intro, *scenes = parts
    return dict(
        intro=intro,
        scenes=scenes
        )

def group_scenes_into_acts(data):
    acts = []

    for scene in data['scenes']:
        heading = scene[0]
        assert heading.tag in ('h1', 'h2'), heading
        if heading.tag == 'h1':
            act = {
                'scenes': []
            }
            acts.append(act)
        print(heading.text, heading.tag)
        print(act)

        act['scenes'].append(scene)

    del data['scenes']
    data['acts'] = acts
    return data

def split_scene_into_heading_and_rest(scene):
    newlines = scene.text
    heading = scene[0]

    assert heading.tag in ('h1', 'h2'), heading
    assert re.match(r'\n+', newlines), newlines

    scene_text = ElementTree.tostring(element=scene, encoding='unicode')

    scene = re.match(r'\n+(.+?)\n\n(.+)', scene_text, flags=re.DOTALL)
    scene = {
        'heading': heading.text,
        'text': scene_text
        }

    return scene

def split_scenes_into_heading_and_rest(data):
    data['acts'] = [
        {
            'scenes': [split_scene_into_heading_and_rest(s)
            for s in act['scenes']]
        }
        for act in data['acts']
        ]

    return data


filters = [
    remove_tab_char,
    replace_tab_tags,
    remove_page_breaks,
    lambda d: enclose_in_xml_tag(d, 'book'),
    parse_xml,
    find_intro_and_scenes,
    group_scenes_into_acts,
    split_scenes_into_heading_and_rest,
]

if __name__ == '__main__':
    with open('data/Hamlet/svensk.txt') as f:
        data = f.read()

    result = apply_filters(filters, data)
    # print(result)

    # with open('out.json', 'w') as f:
    #     print(result, file=f)
        # json.dump(result, f)
