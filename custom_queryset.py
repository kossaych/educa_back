from serialiser import Serializer
from django.db import models

# custom queryset (override queryset class)
class QuerySetWithSerializeOption(models.QuerySet):
    # serialisation function => return a dict
    def serialize(self,**fields) :
        serializer = Serializer(self,**fields)
        data = serializer.serialize()
        return data
