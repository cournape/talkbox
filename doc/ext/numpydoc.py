import os, re
from docscrape_sphinx import SphinxDocString, SphinxClassDoc, SphinxFunctionDoc
import inspect

def mangle_docstrings(app, what, name, obj, options, lines,
                      reference_offset=[0]):
    if what == 'class':
        lines[:] = str(SphinxClassDoc(obj, '',
                                      func_doc=SphinxFunctionDoc)).split("\n")
    elif what in ('function', 'method'):
        lines[:] = str(SphinxFunctionDoc(obj, '')).split("\n")
    elif what == 'module':
        pass
    else:
        lines[:] = str(SphinxDocString(obj.__doc__)).split("\n")

    if app.config.numpydoc_edit_link and hasattr(obj, '__name__') and \
           obj.__name__:
        v = dict(full_name=obj.__name__)
        lines += ['', app.config.numpydoc_edit_link % v]

    # replace reference numbers so that there are no duplicates
    references = []
    for l in lines:
        l = l.strip()
        if l.startswith('.. ['):
            references.append(int(l[len('.. ['):l.index(']')]))

    # Start renaming from the biggest number, otherwise we may
    # overwrite references.
    references.sort()
    if references:
        for i, line in enumerate(lines):
            for r in references:
                new_r = reference_offset[0] + r
                lines[i] = lines[i].replace('[%d]_' % r,
                                            '[%d]_' % new_r)
                lines[i] = lines[i].replace('.. [%d]' % r,
                                            '.. [%d]' % new_r)

    reference_offset[0] += len(references)

def initialize(app):
    monkeypatch_sphinx_ext_autodoc()

    fn = app.config.numpydoc_phantom_import_file
    if (fn and os.path.isfile(fn)):
        print "[numpydoc] Phantom importing modules from", fn, "..."
        import_phantom_module(fn)

def setup(app):
    app.connect('autodoc-process-docstring', mangle_docstrings)
    app.connect('builder-inited', initialize)
    app.add_config_value('numpydoc_phantom_import_file', None, True)
    app.add_config_value('numpydoc_edit_link', None, True)

    app.add_directive('autosummary', autosummary_directive, 1, (0, 0, False))

#------------------------------------------------------------------------------
# .. autosummary::
#------------------------------------------------------------------------------
from docutils.statemachine import ViewList
from docutils import nodes

def autosummary_directive(dirname, arguments, options, content, lineno,
                          content_offset, block_text, state, state_machine):
    names = []
    names += [x for x in content if x.strip()]
    
    result, warnings = get_autosummary(names, state.document)

    node = nodes.paragraph()
    state.nested_parse(result, 0, node)
    
    return warnings + node.children

def get_autosummary(names, document):
    result = ViewList()
    warnings = []

    prefixes = ['']
    prefixes.append(document.settings.env.currmodule)

    max_name_len = max(map(len, names)) + 7
    link_fmt = '%%-%ds' % max_name_len

    table_banner = ('='*max_name_len) + '  ' + '==============='
    result.append(table_banner, '<autosummary>')
    
    for name in names:
        try:
            obj = import_by_name(name, prefixes=prefixes)
            doclines = obj.__doc__.split("\n")
        except ImportError:
            warnings.append(document.reporter.warning(
                'failed to import %s' % name))
            continue
        
        while doclines and (not doclines[0].strip()
                            or re.search(r'[\w.]\(.*\)', doclines[0])):
            doclines = doclines[1:] # skip possible signature or empty lines

        if doclines:
            result.append((link_fmt + "  %s") % (":obj:`%s`" % name,
                                                 doclines[0].strip()),
                          '<autosummary>')
        else:
            result.append(link_fmt % name, '<autosummary>')
    result.append(table_banner, '<autosummary>')
    result.append('', '<autosummary>')

    return result, warnings

def import_by_name(name, prefixes=['']):
    for prefix in prefixes:
        try:
            return _import_by_name('.'.join([prefix, name]))
        except ImportError:
            pass
    raise ImportError

def _import_by_name(name):
    try:
        name_parts = name.split('.')
        last_j = 0
        modname = None
        for j in reversed(range(1, len(name_parts)+1)):
            last_j = j
            modname = '.'.join(name_parts[:j])
            try:
                __import__(modname)
            except ImportError:
                continue
            if modname in sys.modules:
                break

        if last_j < len(name_parts):
            obj = sys.modules[modname]
            for obj_name in name_parts[last_j:]:
                obj = getattr(obj, obj_name)
            return obj
        else:
            return sys.modules[modname]
    except (ValueError, ImportError, AttributeError, KeyError), e:
        raise ImportError(e)

#------------------------------------------------------------------------------
# Monkeypatch sphinx.ext.autodoc to accept argspecless autodocs
#------------------------------------------------------------------------------

def monkeypatch_sphinx_ext_autodoc():
    global _original_format_signature
    import sphinx.ext.autodoc

    if sphinx.ext.autodoc.format_signature is our_format_signature:
        return

    print "[numpydoc] Monkeypatching sphinx.ext.autodoc ..."
    _original_format_signature = sphinx.ext.autodoc.format_signature
    sphinx.ext.autodoc.format_signature = our_format_signature

SIGNATURE_RE = re.compile('\(.*\)', re.I)

def our_format_signature(what, obj):
    try:
        if not callable(obj): return ''
        if hasattr(obj, '__argspec_is_invalid_'): raise TypeError()

        # Do not try to inspect classes that don't define `__init__`
        if inspect.isclass(obj) and \
           'initializes x; see ' in obj.__init__.__doc__:
            return ''

        return _original_format_signature(what, obj)
    except TypeError:
        if not hasattr(obj, '__doc__'): raise
        doclines = obj.__doc__.strip().split("\n")
        if SIGNATURE_RE.search(doclines[0]):
            sig = re.sub("^[^(]*", "", doclines[0])
            doc = "\n".join(doclines[1:]).strip()
            return sig
        else:
            raise

#------------------------------------------------------------------------------
# Creating 'phantom' modules from an XML description
#------------------------------------------------------------------------------
import imp, sys, compiler, types

def import_phantom_module(xml_file):
    import lxml.etree as etree

    object_cache = {}

    tree = etree.parse(xml_file)
    root = tree.getroot()

    dotsort = lambda x: x.attrib['id'].count('.')

    # Create phantom items
    for node in sorted(root, key=dotsort):
        name = node.attrib['id']
        doc = (node.text or '').decode('string-escape') + "\n"

        # create parent, if missing
        parent = name
        while True:
            parent = '.'.join(parent.split('.')[:-1])
            if not parent: break
            if parent in object_cache: break
            obj = imp.new_module(parent)
            object_cache[parent] = obj
            sys.modules[parent] = obj
        
        # create object
        if node.tag == 'module':
            obj = imp.new_module(name)
            obj.__doc__ = doc
            sys.modules[name] = obj
        elif node.tag == 'class':
            obj = type(name, (), {'__doc__': doc})
        elif node.tag == 'callable':
            funcname = node.attrib['id'].split('.')[-1]
            argspec = node.attrib.get('argspec')
            if argspec:
                argspec = re.sub('^[^(]*', '', argspec)
                doc = "%s%s\n\n%s" % (funcname, argspec, doc)
            obj = lambda: 0
            obj.__argspec_is_invalid_ = True
            obj.func_name = funcname
            obj.__name__ = name
            obj.__doc__ = doc
        else:
            class Dummy(object): pass
            obj = Dummy()
            obj.__name__ = name
            obj.__doc__ = doc
        object_cache[name] = obj
        
        if parent:
            obj.__module__ = parent
            setattr(object_cache[parent], name.split('.')[-1], obj)

    # Populate items
    for node in root:
        obj = object_cache.get(node.attrib['id'])
        if obj is None: continue
        for ref in node.findall('ref'):
            setattr(obj, ref.attrib['name'],
                    object_cache.get(ref.attrib['ref']))
