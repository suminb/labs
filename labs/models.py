import os
import yaml


class DocumentStatus(object):
    current = 'current'
    discontinued = 'discontinued'


class Document(object):
    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def load(cls, page_name, status=DocumentStatus.current):
        path = os.path.join('labs', 'docs', status, page_name + '.yml')
        with open(path) as fin:
            return Document(page_name=page_name, **yaml.load(fin.read()))

    @classmethod
    def load_all(cls, status=DocumentStatus.current):
        dir_path = os.path.join('labs', 'docs', status)
        for path in os.listdir(dir_path):
            if path.endswith('.yml'):
                basename = os.path.basename(path)
                page_name = os.path.splitext(basename)[0]
                yield cls.load(page_name)

    def dump(self):
        attrs = [attr for attr in dir(self) if not attr.startswith('__')]
        return {attr: getattr(self, attr) for attr in attrs}

    @property
    def link(self):
        """Returns the first element in the 'links' property. Returns None
        if 'links' has no element.
        """
        return self.links[0]
