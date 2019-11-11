from datetime import datetime

from mongoengine import document, fields


class Document(document.Document):
    created = fields.DateTimeField()
    modified = fields.DateTimeField()

    meta = {
        'abstract': True,
    }

    def save(self, *args, **kwargs):
        if not self.created:
            self.created = datetime.utcnow()

        self.modified = datetime.utcnow()
        return super().save(*args, **kwargs)

    def update(self, **kwargs):
        kwargs.update({'modified': datetime.utcnow()})
        return super().update(**kwargs)