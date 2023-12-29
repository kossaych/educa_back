 
class Serializer:
    def __init__(self, query_set, **fields):
        self.query_set = query_set 
        self.fields = fields
        self.json_data = []
    
    def serialize(self) :
     #   if len(self.query_set) == 0 : return []
        if not self.is_iterable(self.query_set):
            self.json_data =  self.handle_object(self.query_set)
        else : 
            for obj in self.query_set :
                self.json_data.append(self.handle_object(obj))
            #self.handle_query_set()

        return self.json_data
  
    def handle_object (self,obj):
            json_object = {}      
            selected_fields = self.selected_fields(obj)
            
            for field_name, field in selected_fields:
                
                if   isinstance(field,FunctionSerializer):
                     json_object[field_name] = self.handle_function(obj, field)         
                
                elif isinstance(field,RelatedFieldSerializer):
                     json_object[field_name] = self.handle_related_field(obj, field)
                elif isinstance(field,FieldSerializer) :
                    json_object[field_name] = self.handle_field(obj,field)
                elif type(field) in [str,bool,int,float,set,list,dict,tuple] :
                    json_object[field_name] = field
                else :
                    raise(ValueError('invalid field type'))
            
            return json_object
    
    def selected_fields (self,obj) :
        
        if self.fields == {} :
            selected_fields = self.get_default_fields(obj)
        else :
            selected_fields = self.fields.items()
        
        return selected_fields
    @staticmethod
    def is_iterable(obj):
    
        try:
            iter(obj)
            return True
        except TypeError:
            return False
    @staticmethod
    def get_default_fields(obj):
        print(type(obj),obj._meta)
        return {field.name: FieldSerializer(field.name) for field in obj._meta.fields}.items()
   
   
    @staticmethod
    def handle_field(obj,field) :
        return str(getattr(obj, str(field.field)))
    @staticmethod
    def handle_function(obj, field): 
         
        function = field.function
       
         
            
        function = getattr(obj, function)
        result = function(*field.args_params,**field.kwargs_params)
    
        if type(result) in [str,bool,int,float,set,list,dict,tuple] :
                return result
        else :
            fields = field.fields
            filters = field.filters
            try :
                result = result.filter(**filters)
            except :
                pass
            serializer = Serializer(result,**fields)
            return serializer.serialize()         
    @staticmethod
    def handle_related_field(obj, field):
        filters = field.filters
        try :
            related_model = field.model
        except :
            related_model = None
        if (related_model != None) :
            related_object = related_model.objects.filter(
                **{field.related_field : obj},
                **filters
            )                                                         
        else :
            from django.db.models.fields.reverse_related import OneToOneRel
            related_objects = obj._meta.related_objects              
            related_oneto_one_objects_names = [rel_obj.get_cache_name() for rel_obj in related_objects if type(rel_obj) == OneToOneRel]
                       
            if field.related_field in related_oneto_one_objects_names :
                try : 
                    related_object = getattr(obj, field.related_field)
                except : 
                    return {}
            else :   
                related_object = getattr(obj, field.related_field)
        try :
            data = related_object.serialize(**field.fields)
        except : 
            data = related_object.all().serialize(**field.fields)

        return data

class BaseSerializer :
    def __init__(self):
        self.fields = {}
        self.filters = {}
    def set_fields(self,**fields) :
        self.fields = fields
        return self
    def set_filters(self, **filters):
        self.filters = filters
        return self
      
class RelatedFieldSerializer(BaseSerializer) :
    def __init__(self,related_field,model = None):
        super().__init__()
        self.related_field = related_field 
        if model != None :
            self.model = model

class FunctionSerializer(BaseSerializer) :
    def __init__(self,function, *args_params,**kwargs_params) :
        super().__init__() 
        self.function = function
        self.args_params = args_params
        self.kwargs_params = kwargs_params

class FieldSerializer :
    def __init__(self,field) :
        self.field = field
   

