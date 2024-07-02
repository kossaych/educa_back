from typing import Any
from custom_queryset import QuerySetWithSerializeOption
from django.db import models
from serialiser import Serializer

# an abstract model to add serialisation option to other models
class ModelWithSerializeOption(models.Model):
    # change the manager to a add new queryset options
    class Meta :
        abstract =True 
    objects = QuerySetWithSerializeOption.as_manager()
    def serialize(self,**fields) :
        serializer = Serializer(self,**fields)
        data = serializer.serialize()
        return data
"""class RelatedManagerWithSerializeOption :
    def __call__(self) :
        return QuerySetWithSerializeOption.as_manager()"""