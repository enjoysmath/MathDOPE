from neomodel import (StructuredNode, StructuredRel, IntegerProperty,
                      StringProperty, BooleanProperty, One, OneOrMore, 
                      ZeroOrMore, FloatProperty, UniqueIdProperty, 
                      RelationshipTo)
#from django_neomodel import DjangoNode
#from django.db import models
from dope.settings import MAX_ATOMIC_LATEX_LENGTH, DEFAULT_CATEGORY_NAME, MAX_DIAGRAM_NAME_LEN, MAX_SLUG_LEN
from django.core.exceptions import ObjectDoesNotExist
from neomodel import db
from dope.python_tools import deep_get
from dope.variable import Variable
from dope.keyword import Keyword
from database.neo4j_tools import neo4j_escape_regex_str 

    
class Arrow(StructuredRel):    
    # RE-DESIGN: TODO - these need to be independent of style and settable in an accompanying
    # panel to the editor.
    # These are the mathematical properties, that you can search by:
    #epic = BooleanProperty(default=False)
    #monic = BooleanProperty(default=False)
    #inclusion = BooleanProperty(default=False)
    name = StringProperty(max_length=MAX_ATOMIC_LATEX_LENGTH, default='')
    diagram_index = IntegerProperty(required=True)    
    
    # Strictly style below this line:   
    NUM_LINES = { 1: 'one', 2: 'two', 3: 'three' }
    num_lines = IntegerProperty(choices=NUM_LINES, default=1)

    LeftAlign, CenterAlign, RightAlign, OverAlign = range(4)
    DefaultAlignment = LeftAlign    
     
    ALIGNMENT = { 0:LeftAlign,  1:RightAlign, 2:CenterAlign, 3:OverAlign}
    alignment = IntegerProperty(choices=ALIGNMENT, default=DefaultAlignment)
    
    label_position = IntegerProperty(default=50)
    offset = IntegerProperty(default=0)
    curve = IntegerProperty(default=0)
    tail_shorten = IntegerProperty(default=0)
    head_shorten = IntegerProperty(default=0)
    
    TAIL_STYLE = {0:'none', 1:'mono', 2:'hook', 3:'arrowhead', 4:'CONNECTS_TO'}
    tail_style = IntegerProperty(choices=TAIL_STYLE, default=0)
        
    SIDE = {0:'none', 1:'top', 2:'bottom'}
    hook_tail_side = IntegerProperty(choices=SIDE, default=0)    
    
    HEAD_STYLE = {0:'none', 1:'arrowhead', 2:'epi', 3:'harpoon'}
    head_style = IntegerProperty(choices=HEAD_STYLE, default=1)
    harpoon_head_side = IntegerProperty(choices=SIDE, default=0)
    
    BODY_STYLE = {0:'solid', 1:'none', 2:'dashed', 3:'dotted', 4:'squiggly', 5:'barred'}
    body_style = IntegerProperty(choices=BODY_STYLE, default=0)
    
    color_hue = IntegerProperty(default=0)
    color_sat = IntegerProperty(default=0)   # BUGFIX: default (black) is 0,0,0 in hsl, not 0,100,0
    color_lum = IntegerProperty(default=0)
    color_alph = FloatProperty(default=1.0)
    
    def copy_properties_from(self, f, nodes_memo):
        self.name = f.name
        self.diagram_index = f.diagram_index
        self.num_lines = f.num_lines
        self.alignment = f.alignment
        self.label_position = f.label_position
        self.offset = f.offset
        self.curve = f.curve
        self.tail_shorten = f.tail_shorten
        self.head_shorten = f.head_shorten
        self.tail_style = f.tail_style
        self.hook_tail_side = f.hook_tail_side
        self.head_style = f.head_style
        self.harpoon_head_side = f.harpoon_head_side
        self.body_style = f.body_style
        self.color_hue = f.color_hue
        self.color_sat = f.color_sat
        self.color_lum = f.color_lum
        self.color_alph = f.color_alph
        self.save()
        
    def load_from_editor(self, format):
        if len(format) > 2:
            self.name = format[2]
        else:
            self.name = ''   # BUGFIX: need this
        
        if len(format) > 3:
            self.alignment = format[3]
        
        if len(format) > 4:                
            options = format[4]            
            self.label_position = options.get('label_position', 50)
            self.offset = options.get('offset', 0)
            self.curve = options.get('curve', 0)
            shorten = options.get('shorten', {'source': 0, 'target': 0})
            self.tail_shorten = shorten.get('source', 0)
            self.head_shorten = shorten.get('target', 0)
            self.num_lines = options.get('level', 1)
            
            self.body_style = next(x for x,y in self.BODY_STYLE.items() \
                                   if y == deep_get(options, ('style', 'body', 'name'), 'solid'))
            
            self.tail_style = next(x for x,y in self.TAIL_STYLE.items() \
                                   if y == deep_get(options, ('style', 'tail', 'name'), 'none' ))
            
            side = deep_get(options, ('style', 'tail', 'side'), 'none')
            
            if isinstance(side, int):
                self.hook_tail_side = side
            else:
                self.hook_tail_side = next(x for x,y in self.SIDE.items() if y == side)
            
            self.head_style = next(x for x,y in self.HEAD_STYLE.items() \
                                   if y == deep_get(options, ('style', 'head', 'name'), 'arrowhead'))
            
            side = deep_get(options, ('style', 'head', 'side'), 'none')
            
            if isinstance(side, int):
                self.harpoon_head_side = side
            else:
                self.harpoon_head_side = next(x for x,y in self.SIDE.items() if y == side)
                
            if len(format) > 5:
                color = format[5]
            elif 'colour' in options:
                color = options['colour']
            else:
                color = [0, 0, 0, 1.0]  # BUGFIX: black is hsl:  0,0,0 not 0,100,0
                
            self.color_hue = color[0]
            self.color_sat = color[1]
            self.color_lum = color[2]
            
            if len(color) > 3:
                self.color_alph = color[3]            
        
        self.save()
        
    def quiver_format(self):
        format = [self.source.diagram_index, self.target.diagram_index]
        format.append(self.name if self.name is not None else '')
        format.append(self.alignment)
        options = {
            #'colour' : [self.color_hue, self.color_sat, self.color_lum, self.color_alph],
            'label_position': self.label_position,
            'offset' : self.offset,
            'curve' : self.curve,
            'shorten' : {
                'source' : self.tail_shorten,
                'target' : self.head_shorten,
            },
            'level' : self.num_lines,
            'style' : {
                'tail': {
                    'name' : self.TAIL_STYLE[self.tail_style],
                    'side' : self.SIDE[self.hook_tail_side],
                },
                'head': {
                    'name' : self.HEAD_STYLE[self.head_style],
                    'side' : self.SIDE[self.harpoon_head_side],
                },
                'body': {
                    'name' : self.BODY_STYLE[self.body_style],
                }                    
            },
            'colour' : [self.color_hue, self.color_sat, self.color_lum, self.color_alph],
        }
        format.append(options)
        format.append([self.color_hue, self.color_sat, self.color_lum, self.color_alph])
        return format
    
    @property
    def target(self):
        return Object.nodes.get_or_none(uid=self.end_node().uid)
    
    @property
    def source(self):
        return Object.nodes.get_or_none(uid=self.start_node().uid)


class Object(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(max_length=MAX_ATOMIC_LATEX_LENGTH, required=True)
    CONNECTS_TO = RelationshipTo('Object', 'CONNECTS_TO', model=Arrow, cardinality=ZeroOrMore)    
    diagram_index = IntegerProperty(required=True)

    # Position & Color:
    x = IntegerProperty(default=0)
    y = IntegerProperty(default=0) 
    
    color_hue = IntegerProperty(default=0)
    color_sat = IntegerProperty(default=0)
    color_lum = IntegerProperty(default=0)
    color_alph = FloatProperty(default=1.0) 
            
    @staticmethod
    def create_model(**kwargs):
        raise NotImplementedError    
    
    @staticmethod
    def our_create(**kwargs):
        ob = Object(**kwargs).save()
        return ob
    
    #def copy(self, nodes_memo, **kwargs):
        #copy = Object.our_create(**kwargs, diagram_index=self.diagram_index)
        #nodes_memo[copy.diagram_index] = copy
        #copy.name = self.name
        #copy.x = self.x
        #copy.y = self.y
        #copy.color_hue = self.color_hue
        #copy.color_sat = self.color_sat
        #copy.color_lum = self.color_lum
        #copy.alph = self.color_alph
                
        #for f in self.all_morphisms():
            #x = f.end_node()
            #if x.diagram_index not in nodes_memo:
                #x.copy(nodes_memo)
            #y = nodes_memo[x.diagram_index]
            #f1 = copy.morphisms.connect(y)
            #f1.copy_properties_from(f, nodes_memo)  # Calls save()
            
        #copy.save()
        
        #return copy    
    
    def __repr__(self):
        return f'Object("{self.name}")'
    
    def all_outgoing_arrows(self):
        query = \
            f"MATCH (X:Object)-[r:CONNECTS_TO]->(:Object)" \
            f"WHERE X.uid='{self.uid}' " \
            f"RETURN r"
        
        results, meta = db.cypher_query(query)
        
        print("DEBUG/CYPHER QUERY: ", query)
        
        return [Arrow.inflate(row[0]) for row in results]
                    
    def delete(self):
        # Delete all the outgoing morphisms first:
        db.cypher_query(f"MATCH (X:Object)-[r:CONNECTS_TO]->(:Object)"
                        f"MATCH (f:Arrow) "
                        f"WHERE X.uid='{self.uid}' AND f.uid=r.uid DETACH DELETE f, r")  
        # TODO: see if we need to also delete r here ("DELETE r,f"), or whether the following automatically deletes it:
        super().delete()
           
    @staticmethod
    def create_from_editor(format, index:int):
        o = Object(diagram_index=index)
        o.init_from_editor(format, index)
        return o
        
    def init_from_editor(self, format, index):
        o = self
        o.x = format[0]
        o.y = format[1]
        
        if len(format) > 2:
            o.name = format[2]
            
        if len(format) > 3:
            color = format[3]
            o.color_hue = color[0]
            o.color_sat = color[1]
            o.color_lum = color[2]
            o.color_alph = color[3]
        
        o.save()   
        return o
    
    def quiver_format(self):
        return [self.x, self.y, self.name, 
                [self.color_hue, self.color_sat, self.color_lum, self.color_alph]]
        
        
class Diagram(StructuredNode):  
    #"""
    #Models should be decouple (inheritance rarely used)
    #Otherwise basic seeming queries return all types in the hierarchy.
    #Hence just StructuredNode here.
    #"""
   
    uid = UniqueIdProperty()
    name = StringProperty(max_length=MAX_DIAGRAM_NAME_LEN, default='?')
    slug = StringProperty(required=True)
    author_id = IntegerProperty(required=True)
    objects = RelationshipTo('Object', 'HAS_OBJECT', cardinality=ZeroOrMore)       
    
    def morphism_count(self):
        count = 0
        for x in self.all_objects():
            count += len(x.morphisms)
        return count
    
    def copy(self, **kwargs):
        copy = Diagram.our_create(**kwargs)
        
        nodes_memo = {}
        
        for x in self.all_objects():
            if x.diagram_index not in nodes_memo:
                x.copy(nodes_memo)
        
        for x in nodes_memo.values():  # BUGFIX: need to consider all nodes added in subcalls, secondly
            copy.objects.connect(x)
            
        copy.save()                    
        return copy
                
    @property
    def commutes_text(self):
        return self.COMMUTES[self.commutes]
    
    #@property
    #def commutes(self):
        #return self.COMMUTES[self.commutative]
    
    #@commutes.setter
    #def commutes(self, text):
        #for key, val in self.COMMUTES.items():
            #if text == val:
                #self.commutative = key
                #break
        #else:
            #raise ValueError(f'There are only {len(self.COMMUTES)} possible options for Diagram.commutes')
    
    @staticmethod
    def our_create(**kwargs):
        diagram = Diagram(**kwargs).save()
        Diagram.init_diagram(diagram)
        return diagram
        
    @staticmethod
    def init_diagram(diagram):
        #category = get_unique(Category, name=DEFAULT_CATEGORY_NAME)
        #diagram.category.connect(category)
        diagram.save()  
        
    def quiver_format(self):
        edges = []
        vertices = []
        
        objects = list(self.all_objects())
        objects.sort(key=lambda x: x.diagram_index)        
        
        for o in objects:
            vertices.append(o.quiver_format())
            for f in o.all_outgoing_arrows():
                edges.append(f.quiver_format())
                    
        format = [0, len(vertices)]
        format += vertices
        format += edges
        
        return format
    
    def load_from_editor(self, format):
        obs = []
        vertices = format[2:2 + format[1]]
        
        for k,v in enumerate(vertices):
            o = Object.create_from_editor(v, k)
            obs.append(o)
        
        edges = format[2 + format[1]:]
            
        for k,e in enumerate(edges):
            A = obs[e[0]]
            B = obs[e[1]]
            f = A.CONNECTS_TO.connect(B, {'diagram_index': k})
            f.save()
            f.load_from_editor(e)
            A.save()
            f.save()
            
        self.add_objects(obs)               
    
    def all_objects(self):
        results, meta = db.cypher_query(
            f'MATCH (D:Diagram)-[:HAS_OBJECT]->(x:Object) WHERE D.uid="{self.uid}" RETURN x')
        return [Object.inflate(row[0]) for row in results]
        
    def delete_objects(self):
        for o in self.all_objects():
            o.delete()
        self.save()
        
    def add_objects(self, obs):
        for o in obs:
            self.objects.connect(o)
        self.save()
        
    @staticmethod
    def get_paths_by_length(diagram_uid):
        paths_by_length = \
            f"MATCH (D:Diagram)-[:HAS_OBJECT]->(X:Node), " + \
            f"p=(X)-[:CONNECTS_TO*]->(:Node) " + \
            f"WHERE D.uid = '{diagram_uid}' " + \
            f"RETURN p " + \
            f"ORDER BY length(p) DESC" 
        
        paths_by_length, meta = db.cypher_query(paths_by_length)
        
        return paths_by_length
                          
        ## TODO: test code with doublequote in template_regex ^^^        
        
    @staticmethod
    def build_query_from_paths(paths):
        nodes = {
            # Keyed by Object.diagram_index, value is Object
        }
        rels = {
            # Keyed by Morphism.diagram_index, value is Morphism
        }

        search_query = ''
               
        for path in paths:
            path = path[0]   # [0] is definitely needed here
            node = Object.inflate(path.start_node)
            
            search_query += f"(n{node.diagram_index}:Node)"
            
            if node.diagram_index not in nodes:
                nodes[node.diagram_index] = node
            
            add_query = ''
            
            for rel in path.relationships:
                rel = Arrow.inflate(rel)
                #rel = get_model_by_uid(Arrow, uid=rel.uid)
                
                if rel.diagram_index not in rels:
                    rels[rel.diagram_index] = rel
                    
                    add_query += f"-[r{rel.diagram_index}:CONNECTS_TO]->"
                    next_node = rel.end_node()  # BUGFIX: no need to inflate here
                    add_query += f"(n{next_node.diagram_index}:Node)"
                    
                    # BUGFIX: don't forget to add the next node into nodes:
                    if next_node.diagram_index not in nodes:
                        nodes[next_node.diagram_index] = next_node
            
            if add_query:      
                search_query += add_query
                
            search_query += ', '
        
        if search_query:
            search_query = search_query[:-2]
        return nodes, rels, search_query
    
    @staticmethod
    def build_match_query(query, nodes, rels):
        query = "MATCH " + query            
        
        template_regexes = {
            # Keyed by node or relationship .name property, values are 
            # (template, neo4j regex)
        }
        
        #var_mapping = {
            ## Keyed by variable object, value is list of tuples (node or rel, template_index)
        #}
        
        def neo4j_regex_from_template(template):
            regex = ""
            for piece in template:
                if isinstance(piece, Variable):
                    regex += ".+"
                elif isinstance(piece, Keyword):
                    regex += neo4j_escape_regex_str(str(piece))
                else:  # str
                    regex += neo4j_escape_regex_str(piece)                
            return regex   
                    
        for node in nodes.values():
            name = node.name
            
            if name not in template_regexes:
                template, vars = Variable.parse_into_template(name)
                regex = neo4j_regex_from_template(template)
                template_regexes[name] = (template, regex)
                
        for rel in rels.values():
            name = rel.name
            
            if name not in template_regexes:
                template, vars = Variable.parse_into_template(name)
                regex = neo4j_regex_from_template(template)
                template_regexes[name] = (template, regex)       
        
        query += " WHERE "
        
        for index, node in nodes.items():
            query += f"n{index}.uid =~ '{template_regexes[node.uid][1]}' AND "
            
        if rels:
            for index, rel in rels.items():
                query += f"r{index}.uid =~ '{template_regexes[rel.uid][1]}' AND "
            
        query = query[:-5]   # Remove AND      
        
        return template_regexes, query   



class Category(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(required=True)

    @staticmethod
    def our_create(**kwargs):
        category = Category(**kwargs).save()
        return category


#class Context:
    #diagrams = RelationshipTo('Diagram', 'ENTAILS')
    


##class Proof(StructuredNode):
   
    ##steps = RelationshipTo('ProofStep', 'HAS_STEP', model=ProofOrder, cardinality=OneOrMore)
    ##goal_step = RelationshipTo('ProofStep', 'ENDS_WITH', cardinality=One)


#class ProofStep(StructuredNode):
    #english = StringProperty()
    #output_diagram = RelationshipTo('Diagram', 'OUTPUTS', cardinality=One)
    
    
#class Let(ProofStep):
    #pass


#class Theorem(StructuredNode):
    #name = StringProperty(max_length=MAX_DIAGRAM_NAME_LEN)     # TODO: create another theorem name max variable in settings
    
    #input_diagrams = RelationshipTo('Diagram', 'REQUIRES', model=ProofOrder, cardinality=OneOrMore)
    #output_diagram = RelationshipTo('Diagram', 'OUTPUTS', cardinality=One)
    
    #proofs = RelationshipTo('Proof', 'PROVEN_BY', cardinality=ZeroOrMore)
    

#class TheoremApply(ProofStep):
    #input_diagrams = RelationshipTo('Diagram', 'REQUIRES', model=ProofOrder, cardinality=OneOrMore)
    
    


#class DiagramRule(Arrow):
    #author_id = StringProperty(required=True)
    
    ## Mathematics
    ##functor_id = StringProperty()
    ## The link to an actual known functor, if this rule is factorial, or None otherwise
    ## We will have to be careful when deleting a Functor.  We can only delete it
    ## if there exist no rules referring to it through this property.
    
    #@property
    #def author(self):
        #return 
    
    #@author.setter
    #def author(self, username):
        #if self.author != username:
            #diagram = self.key_diagram.single()
            #diagram.author = username
            #diagram.save()
            #diagram = self.result_diagram.single()
            #diagram.author = username
            #diagram.save()
            #self.checkedOutBy = username
            #self.save()
            
    #def can_be_checked_out(self):
        #return self.key_diagram.single().author is None and \
            #self.result_diagram.single().author is None and \
            #self.author is None
    
    #@staticmethod
    #def our_create(key=None, res=None, **kwargs):
        #if key is None:
            #key = 'Key'
        #if res is None:
            #res = 'Result'
            
        ##cat = get_unique(Category, name='Any')    
        #source = Diagram(name=key).save()
        ##source.category.connect(cat)
        #source.save()
        #target = Diagram(name=res).save()
        ##target.category.connect(cat)
        #target.save()
        #rule = DiagramRule(**kwargs)
        #rule.save()
        #rule.key_diagram.connect(source)
        #rule.result_diagram.connect(target)
        #rule.save()
        #return rule
        
    ##@staticmethod
    ##def get_variable_mapping(source:Diagram, target:Diagram) -> dict:
        ##map = {}
        
        ##for x in source.all_objects():
            ##template, vars = Variable.parse_template(text)
                
    ##def get_variable_template_regex(self, text:str) -> bidict:    




model_str_to_class = {
    'Object' : Object,
    'Diagram' : Diagram,
    #'DiagramRule' : DiagramRule,
}

#MAX_MODEL_CLASS_NAME_LENGTH = max([len(x) for x in model_str_to_class.keys()])

def get_model_class(Model:str):
    if len(Model) > MAX_ATOMIC_LATEX_LENGTH:
        return ValueError("You're passing in an unimplemented Model string.")        
    
    if Model not in model_str_to_class:
        raise NotImplementedError(f'Model {Model} has no entry in a certain table.')
    
    Model = model_str_to_class[Model]    
    return Model


def get_model_by_slug(Model, slug:str):
    if len(slug) > MAX_SLUG_LEN:
        raise ValueError(f'That {Model} name is longer than {MAX_TEXT_LENGTH} characters.')
    
    if isinstance(Model, str):
        Model = get_model_class(Model)
        
    model = Model.nodes.get_or_none(slug=slug)
    
    if model is None:
        raise ObjectDoesNotExist(f'An instance of the {Model} with name "{slug}" does not exist.')
    
    return model


def get_model_by_uid(Model, uid:str):
    if len(uid) > 36:
        raise ValueError('That id is longer than a UUID4 is supposed to be.')
    
    if isinstance(Model, str):
        Model = get_model_class(Model)
        
    model = Model.nodes.get_or_none(uid=uid)    
    
    if model is None:
        raise ObjectDoesNotExist(f'An instance of the {Model} with uid "{uid}" does not exist.')
    
    return model
                    
                    
def get_unique(Model, **kwargs):
    model = Model.nodes.get_or_none(**kwargs)
    
    if model is None:
        model = Model.our_create(**kwargs)
        model.save()
        
    return model