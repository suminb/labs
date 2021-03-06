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
    def manifest(cls):
        with open(os.path.join('labs', 'docs.yml')) as fin:
            return yaml.load(fin.read())

    @classmethod
    def load(cls, page_name):
        path = os.path.join('labs', 'docs', page_name + '.yml')
        with open(path) as fin:
            return Document(page_name=page_name, **yaml.load(fin.read()))

    @classmethod
    def load_all(cls, status=DocumentStatus.current):
        manifest = cls.manifest()

        for page_name in manifest[status]['pages']:
            yield cls.load(page_name)

    def dump(self):
        attrs = [attr for attr in dir(self) if not attr.startswith('__')]
        return {attr: getattr(self, attr) for attr in attrs}

    @property
    def link(self):
        """Returns the first element in the 'links' property. Returns None
        if 'links' has no element.
        """
        try:
            return self.links[0]
        except (TypeError, IndexError):
            return None
