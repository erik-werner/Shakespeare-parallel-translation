import attr
import json
import re

def apply_filters(filters, data):
    current = data
    for f in filters:
        current = f(current)
    return current

def remove_tab_char(data):
    return data.replace('\t', ' ')

def replace_tab_tags(data):
    return data.replace('<tab>', '\t')

filters = [
    remove_tab_char,
    replace_tab_tags
]

if __name__ == '__main__':
    with open('data/Hamlet/svensk.txt') as f:
        data = f.read()

    result = apply_filters(filters, data)

    with open('out.json', 'w') as f:
        print(result, file=f)
        # json.dump(result, f)
