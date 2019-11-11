from core.models import Document, fields

class Penguin(Document):
    name = fields.StringField()

    def to_dict(self):
        return {
            'id': str(self.id),
            'name': self.name,
        }
