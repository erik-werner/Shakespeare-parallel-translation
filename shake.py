import attr
import json
import re
import xml.etree.ElementTree as ElementTree
from typing import Sequence, Union, Tuple


# @attr.s
# class Intro:
#     text : str

# @attr.s
# class Utterance:
#     text : str

# @attr.s
# class Person:
#     text : str

# @attr.s
# class Text:
#     text : str

# @attr.s
# class Footnote:
#     text : str

# @attr.s
# class SpeechInstruction:
#     children : Sequence[Union[Person, Text]]

# @attr.s
# class Line:
#     children : Sequence[Union[Utterance, SpeechInstruction, Footnote]]

# @attr.s
# class Speaker:
#     text : str

# @attr.s
# class Lines:
#     children : Sequence[Line]

# @attr.s
# class Speech:
#     children : Tuple[Speaker, Lines]

# @attr.s
# class Scene:
#     units : Sequence[Union[Speech, Instruction]]

# @attr.s
# class Act:
#     scenes : Sequence[Scene]

# @attr.s
# class Acts:
#     children : A

# @attr.s
# class Play:
#     parts : Tuple[Intro, Acts]
#     intro : Intro
#     acts : Sequence[Act]




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

def keep_maximum_two_line_breaks(data):
    return re.sub(r'\n\n+', '\n\n', data)

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

        act['scenes'].append(scene)

    del data['scenes']
    data['acts'] = acts
    return data

def split_scene(scene):
    newlines = scene.text
    heading = scene[0]

    assert heading.tag in ('h1', 'h2'), heading
    assert re.match(r'\n+', newlines), newlines

    scene_text = ElementTree.tostring(element=scene, encoding='unicode')

    m = re.match(
        r'^<chapter.+?>\s*<h(1|2)>.+?</h(1|2)>\s+(?P<location>.+?)\n\n(?P<rest>.+)',
        scene_text,
        flags=re.DOTALL
        )

    assert m, scene_text[:100]

    scene = re.match(r'\n+(.+?)\n\n(.+)', scene_text, flags=re.DOTALL)
    scene = {
        'heading': heading.text,
        'location': m.group('location'),
        'units': m.group('rest').split('\n\n')
        }

    return scene

def split_scenes(data):
    data['acts'] = [
        {
            'scenes': [split_scene(s)
            for s in act['scenes']]
        }
        for act in data['acts']
        ]

    return data

# def split_rest_into_units(data):
#     for act in data['acts']:
#         for scene in act['scenes']:
#             scene['units'] = scene['text'].split('\n\n')
#             del scene['text']
#     return data

# def remove_scene_heading_and_find_location(scene):

# def remove_scene_headings_and_find_locations(data):
#     for act in data['acts']:
#         for scene in act['scenes']:
#             scene['units']


filters = [
    keep_maximum_two_line_breaks,
    remove_tab_char,
    replace_tab_tags,
    remove_page_breaks,
    lambda d: enclose_in_xml_tag(d, 'book'),
    parse_xml,
    find_intro_and_scenes,
    group_scenes_into_acts,
    split_scenes,
]

import itertools
import json

if __name__ == '__main__':
    with open('data/Hamlet/svensk.txt') as f:
        data = f.read()

    result = apply_filters(filters, data)

    all_scenes = itertools.chain(*(a['scenes'] for a in result['acts']))
    all_units = itertools.chain(*(s['units'] for s in all_scenes))

    with open('units.json', 'w') as f:
        json.dump(list(all_units), f)

    # print(result)

    # with open('out.json', 'w') as f:
    #     print(result, file=f)
        # json.dump(result, f)
