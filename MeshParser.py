from xml.etree import cElementTree as elemtree
from datetime import date
from collections import defaultdict
import sys


result_list = []

def parse_mesh(filename):
    """Parse a mesh file, successively generating
    `DescriptorRecord` instance for subsequent processing."""
    MeshNameDict = {}
    MeshUiDict = {}

    def tree(): return defaultdict(tree)

    def add(t, path, name, ui):
        for node in path:            
            t = t[node]            
        t['name'] = (name, ui)
        #t['ui'] = ui
        
    MeshTree = tree()

    for _evt, elem in elemtree.iterparse(filename):
        if elem.tag == 'DescriptorRecord':
            #yield DescriptorRecord.from_xml_elem(elem)
            DR = DescriptorRecord.from_xml_elem(elem)

            if DR.tree_numbers != None:
                # make lowercase for Dictionary
                MeshNameDict[DR.name.lower()] = DR.tree_numbers
                MeshUiDict[DR.ui.lower()] = DR.tree_numbers
            
                for item in DR.tree_numbers:
                    add(MeshTree, item.split('.'), DR.name, DR.ui)

    return MeshNameDict, MeshUiDict, MeshTree

def date_from_mesh_xml(xml_elem):
    year = xml_elem.find('./Year').text
    month = xml_elem.find('./Month').text
    day = xml_elem.find('./Day').text
    return date(int(year), int(month), int(day))

class PharmacologicalAction(object):
    """A pharmacological action, denoting the effects of a MeSH descriptor."""
    
    def __init__(self, descriptor_ui):
        self.descriptor_ui = descriptor_ui
    
    @classmethod
    def from_xml_elem(cls, elem):
        descriptor_ui = elem.find('./DescriptorReferredTo/DescriptorUI')
        return cls(descriptor_ui)

class SlotsToNoneMixin(object):
    def __init__(self, **kwargs):
        for attr in self.__slots__:
            setattr(self, attr, kwargs.get(attr, None))
    
    def __repr__(self):
        attrib_repr = ', '.join(u'%s=%r' % (attr, getattr(self, attr)) for attr in self.__slots__)
        return self.__class__.__name__ + '(' + attrib_repr + ')'

class Term(SlotsToNoneMixin):
    """A term from within a MeSH concept."""

    __slots__ = ('term_ui', 'string', 'is_concept_preferred', 'is_record_preferred',
      'is_permuted', 'lexical_tag', 'date_created', 'thesaurus_list')
    
    @classmethod
    def from_xml_elem(cls, elem):
        term = cls()
        term.is_concept_preferred = elem.get('ConceptPreferredYN', None) == 'Y'
        term.is_record_preferred = elem.get('RecordPreferredYN', None) == 'Y'
        term.is_permuted = elem.get('IsPermutedTermYN', None) == 'Y'
        term.lexical_tag = elem.get('LexicalTag')
        for child_elem in elem:
            if child_elem.tag == 'TermUI':
                term.ui = child_elem.text
            elif child_elem.tag == 'String':
                term.name = child_elem.text
            elif child_elem.tag == 'DateCreated':
                term.date_created = date_from_mesh_xml(child_elem)
            elif child_elem.tag == 'ThesaurusIDlist':
                term.thesaurus_list = [th_elem.text for th_elem in child_elem]
        return term

class SemanticType(SlotsToNoneMixin):
    __slots__ = ('ui', 'name')
    
    @classmethod
    def from_xml_elem(cls, elem):
        sem_type = cls()
        for child_elem in elem:
            if child_elem.tag == 'SemanticTypeUI':
                sem_type.ui = child_elem.text
            elif child_elem.tag == 'SemanticTypeName':
                sem_type.name = child_elem.text

class Concept(SlotsToNoneMixin):
    """A concept within a MeSH Descriptor."""
    __slots__ = ( 'ui', 'name', 'is_preferred', 'umls_ui', 'casn1_name', 'registry_num', 
      'scope_note', 'sem_types', 'terms')
    
    @classmethod
    def from_xml_elem(cls, elem):
        concept = cls()
        concept.is_preferred = elem.get('PreferredConceptYN', None) == 'Y'
        for child_elem in elem:
            if child_elem.tag == 'ConceptUI':
                concept.ui = child_elem.text
            elif child_elem.tag == 'ConceptName':
                concept.name = child_elem.find('./String').text
            elif child_elem.tag == 'ConceptUMLSUI':
                concept.umls_ui
            elif child_elem.tag == 'CASN1Name':
                concept.casn1_name = child_elem.text
            elif child_elem.tag == 'RegistryNumber':
                concept.registry_num = child_elem.text
            elif child_elem.tag == 'ScopeNote':
                concept.scope_note = child_elem.text
            elif child_elem.tag == 'SemanticTypeList':
                concept.sem_types = [SemanticType.from_xml_elem(st_elem) for st_elem in child_elem.findall('SemanticType')]
            elif child_elem.tag == 'TermList':
                concept.terms = [Term.from_xml_elem(term_elem) for term_elem in child_elem.findall('Term')]
        return concept

class DescriptorRecord(SlotsToNoneMixin):
    "A MeSH Descriptor Record."""
    
    #__slots__ = ('ui', 'name', 'date_created', 'date_revised', 'pharm_actions', 
    #  'tree_numbers', 'concepts')

    __slots__ = ('ui', 'name', 'tree_numbers')
    
    @classmethod
    def from_xml_elem(cls, elem):
        rec = cls()
        for child_elem in elem:
            if child_elem.tag == 'DescriptorUI':
                rec.ui = child_elem.text
            elif child_elem.tag == 'DescriptorName':
                rec.name = child_elem.find('./String').text
            elif child_elem.tag == 'TreeNumberList':
                rec.tree_numbers = [tn_elem.text for tn_elem in child_elem.findall('TreeNumber')]
            '''
            elif child_elem.tag == 'DateCreated':
                rec.date_created = date_from_mesh_xml(child_elem)
            elif child_elem.tag == 'DateRevised':
                rec.date_revised = date_from_mesh_xml(child_elem)
            elif child_elem.tag == 'TreeNumberList':
                rec.tree_numbers = [tn_elem.text
                  for tn_elem in child_elem.findall('TreeNumber')]
            elif child_elem.tag == 'ConceptList':
                rec.concepts = [Concept.from_xml_elem(c_elem) 
                  for c_elem in child_elem.findall('Concept')]
            elif child_elem.tag == 'PharmacologicalActionList':
                rec.pharm_actions = [PharmacologicalAction.from_xml_elem(pa_elem) 
                  for pa_elem in child_elem.findall('PharmacologicalAction')]
            '''
        return rec

def getTreeNumbers(mesh, disease):

    for data in mesh:
        if data.name == disease:
            return data.tree_numbers

def getTreeData(mesh, disease):

    tree_numbers = []
    result = []

    for data in mesh:
        if data.name == disease:
            tree_numbers = data.tree_numbers
            break

    #for tree_element in tree_numbers:

class Tree(object):
    "Generic tree node."
    def __init__(self, name='root', children=None):
        self.name = name
        self.children = []
        if children is not None:
            for child in children:
                self.add_child(child)
    def __repr__(self):
        return self.name
    def add_child(self, node):
        assert isinstance(node, Tree)
        self.children.append(node)    


def getRootforMeshTree(target_elements, MeshTree):

    t = MeshTree

    for val in target_elements.split('.'):        
        t = t[val]

    return t


def findDiseaseName(t):

    global result_list
    for _, v in t.iteritems():
        #print k,v
        if len(v) == 1:            
            result_list.append(v['name'])            

        if isinstance(v, dict):
          findDiseaseName(v)

def findDiseasePath(disease, MeshNameDic, MeshUiDic, MeshTree, IsUniqueID):

    try : 
        if IsUniqueID == True:
            target_tree = MeshUiDic[disease]
        else:
            target_tree = MeshNameDic[disease]
    except KeyError:
        print "%s : Not Found in XML data" % disease
        sys.exit(0)   

    for idx, treenum in enumerate(target_tree):            
        # only for Diseases
        if not treenum.startswith('C'):
            continue

        t = MeshTree
        treenum_elements = treenum.split('.')
        elements_length = len(treenum_elements)
        #print "%d : " %(idx+1),
        for i, tag in enumerate(treenum_elements):
            #print tag
            if i == elements_length-1:
                print "[%s : %s]" % (t[tag]['name'])
            else:
                #print t[tag]['name'][0], ">",
                print "(%s : %s) > " %(t[tag]['name']),
            #print MeshTree[tag]
            t = t[tag]

def dicts(t):
    try:
        return dict((k, dicts(t[k])) for k in t)
    except TypeError:
        return t

def show_title():

    print "\n\n"
    print " ============= MeshParser v1.0 =================" 
    print "| Find the disease name for input keyword      |"
    print "| - input keyword can be name or uniqueid      |"       
    print " ==============================================="     
    print "\n\n"


if __name__ == '__main__':
    
    argc = len(sys.argv)
    show_title()
    #read_config()

    if argc != 5:
        print "Usage : python MeshParser_v1.py MeSH(xml) keyword direction result_type"
        print "        * keyword     : category or disease name in MeSH / whole / whole-path"
        print "        * direction   : up(categories) / down(dieseases)"
        print "        * result_type : all / unique (for direction down only)"    

        sys.exit(0)

    lasttime = date.today()
    IsUniqueID = False
    
    #1. Make Hash Dict
    MeshName2Dict = {} 
    MeshName2Dict, MeshUi2Dict, MeshTree = parse_mesh(sys.argv[1])
    keyword = sys.argv[2].lower()
    direction = sys.argv[3].lower()
    result_type = sys.argv[4].lower()
    #keyword = sys.argv[3]

    if keyword[0] == 'd' and len(keyword) == 7 and keyword[1:].isdigit():
        # keyword is Unique ID
        IsUniqueID = True


    if keyword == 'whole':
        findDiseaseName(MeshTree)
        
        if result_type == 'all':
            for i in result_list:
                print "%s (%s)" %(i[0], i[1])
        elif result_type == 'unique':
            for i in set(result_list):
                print "%s (%s)" %(i[0], i[1])
        else:
            print "argument error!"
            sys.exit(0)

    elif keyword == 'whole-path':
        findDiseaseName(MeshTree)
        
        for name in set(result_list):            
            findDiseasePath(name[0].lower(), MeshName2Dict, MeshUi2Dict, MeshTree, IsUniqueID)
    else:
        
        if direction == 'up':
            findDiseasePath(keyword, MeshName2Dict, MeshUi2Dict, MeshTree, IsUniqueID)

        elif direction == 'down':
            try: 
                if IsUniqueID == True:
                    target_tree = MeshUi2Dict[keyword]
                else:
                    target_tree = MeshName2Dict[keyword]
            except KeyError:
                print "%s : Not Found in XML data" % keyword
                sys.exit(0)        
                    
            for treenum in target_tree:
                #print "\n[%s]" %(treenum)
                findDiseaseName(getRootforMeshTree(treenum, MeshTree))
                
            #print result_list
            if result_type == 'all':
                for i in result_list:
                    print "%s (%s)" %(i[0], i[1])
                    
            elif result_type == 'unique':
                for i in set(result_list):
                    print "%s (%s)" %(i[0], i[1])
            else:
                print "argument error!"
                sys.exit(0)

        else:
            print "argument error!"
            sys.exit(0)
    #2. Make Tree Structure


    #3. Find all end-nodes for given Keyword


    #4. Get SNP name from ClinVar data

