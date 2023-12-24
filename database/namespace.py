from neomodel import StructuredNode, StringProperty, ZeroOrMore, RelationshipTo
from dope.settings import (MAX_NAMESPACE_LENGTH,)

class Namespace(StructuredNode):    
    identifier = StringProperty(max_length=MAX_NAMESPACE_LENGTH, required=True)
    contains = RelationshipTo('Model', 'CONTAINS', cardinality=ZeroOrMore)
    
    @staticmethod
    def create_namespace(identifier:str):
        if not identifier.isidentifier() or not identifier.replace('-', '_').isidentifier():
            raise ValueError(f'"{identifier}" is not a valid namespace identifier.')        
        return Namespace(identifier=identifier).save()
        
        
            
        
    
    