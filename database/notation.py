from neomodel import StructuredNode, RelationshipTo, One, OneOrMore
from .models import QuiverModel
from .namespace import Namespace
from .runnable_code import Python
        
class Notation(StructuredNode):
    notation_for = RelationshipTo('Model', 'IS_NOTATION_FOR', cardinality=OneOrMore)
    namespace = RelationshipTo('Namespace', 'IS_IN_THE_NAMESPACE', cardinality=OneOrMore)
    python_code = RelationshipTo('Python', 'HAS_PYTHON_CODE', cardinality=OneOrMore)
    #javascript_code = TODO
    
    @staticmethod
    def create_notation(subclass, notation_for:QuiverModel, python_code:Python, namespace:Namespace, **kwargs):
        notation = subclass(notation_for=notation_for, namespace=namespace, 
                            python_code=python_code, **kwargs)
        notation.save()
        return notation        
            
        
class English(Notation):
    @staticmethod
    def create_notation(notation_for:QuiverModel, python_code:Python, namespace:Namespace):
        return Notation.create_notation(English, notation_for, python_code, namespace)
    
    
        