from core.api import APIBase
from temp.models import Penguin

class Main(APIBase):

    def get(self):
        penguins = Penguin.objects()

        return self.res([p.to_dict() for p in penguins])