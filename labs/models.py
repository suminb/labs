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
    def load(cls, name, status=DocumentStatus.current):
        path = os.path.join('labs', 'docs', status, name + '.yml')
        with open(path) as fin:
            return Document(**yaml.load(fin.read()))

    def dump(self):
        attrs = [attr for attr in dir(self) if not attr.startswith('__')]
        return {attr: getattr(self, attr) for attr in attrs}

    @property
    def link(self):
        """Returns the first element in the 'links' property. Returns None
        if 'links' has no element.
        """
        return self.links[0]
