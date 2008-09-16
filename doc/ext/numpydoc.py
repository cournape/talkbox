"""

Numpydoc : adds autodirectives to process docstrings with the Numpy format.

This module is basically Puali Virtanen's with a few modifications:

* The base classes SphinxDocString, SphinxClassDoc and SphinxFunctionDoc
  are PGM's versions.
* If a signature was detected in the docstring, it is removed.
* The format_signature function is now a method of autodoc.RstGenerator,
  (as of Sphinx-0.4dev-20080724)
* As setup calls autodoc.setup, there's no need for registering
  sphinx.ext.autodoc in the conf.py file.



"""


import inspect
import os
import re

from docutils.parsers.rst import directives
from docutils.statemachine import StringList

from sphinx.directives import desc_directive
import sphinx.ext.autodoc as autodoc

from docscraper import NumpyDocString, SphinxDocString, SphinxClassDoc,\
    SphinxFunctionDoc

#-------------------------------------------------------------------------------
#--- .. numpydirectives::
#-------------------------------------------------------------------------------

def numpyfunction_directive(desctype, arguments, options, content, lineno,
                            content_offset, block_text, state, state_machine):

    try:
        doc = SphinxDocString(content, block_format=None, list_format=None)
        sig = doc.extract_signature()
        text = StringList(doc.format())
        
        if sig is not None:
            arguments[0] += sig
        interpreted =  desc_directive('function', arguments, options, text, 
                                      lineno, content_offset, text, state, 
                                      state_machine)
        return interpreted
    except: 
        raise
#        exc_info = sys.exc_info()
#        literal_block = nodes.literal_block(block_text, block_text)
#        return [state_machine.reporter.error('error: %s' % str(exc_info[:2]),
#                                             literal_block,
#                                             line=lineno)]


def numpyclass_directive(desctype, arguments, options, content, lineno,
                         content_offset, block_text, state, state_machine):

    try:
        doc = SphinxDocString(content)
        sig = doc.extract_signature()
        text = StringList(doc.format())
        if sig is not None:
            arguments[0] += sig
        interpreted =  desc_directive('class', arguments, options, text,
                                      lineno, content_offset, text, state,
                                      state_machine)
        return interpreted
    except:
        raise
#        exc_info = sys.exc_info()
#        literal_block = nodes.literal_block(block_text, block_text)
#        return [state_machine.reporter.error('error: %s' % str(exc_info[:2]),
#                                             literal_block,
#                                             line=lineno)]


#------------------------------------------------------------------------------
#--- .. autosummary::
#------------------------------------------------------------------------------
from docutils.statemachine import ViewList
from docutils import nodes
from sphinx import addnodes
from sphinx.util import patfilter
import posixpath

def autosummary_directive(dirname, arguments, options, content, lineno,
                          content_offset, block_text, state, state_machine):
    names = []
    names += [x for x in content if x.strip()]

    result, warnings = get_autosummary(names, state.document)

    node = nodes.paragraph()
    state.nested_parse(result, 0, node)

    env = state.document.settings.env
    suffix = env.config.source_suffix
    all_docnames = env.found_docs.copy()
    dirname = posixpath.dirname(env.docname)

    docnames = []
    doctitles = {}
    for docname in names:
        docname = 'generated/' + docname
        doctitles[docname] = ''
        if docname.endswith(suffix):
            docname = docname[:-len(suffix)]
        docname = posixpath.normpath(posixpath.join(dirname, docname))
        if docname not in env.found_docs:
            warnings.append(state.document.reporter.warning(
                'toctree references unknown document %r' % docname,
                line=lineno))
        docnames.append(docname)

    tocnode = addnodes.toctree()
    tocnode['includefiles'] = docnames
    tocnode['includetitles'] = doctitles
    tocnode['maxdepth'] = -1
    tocnode['glob'] = None

    return warnings + node.children + [tocnode]



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
            doclines = (obj.__doc__ or '').split("\n")
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

def import_by_name(name, prefixes=None):
    for prefix in prefixes or ['']:
        try:
            if prefix:
                prefixed_name = '.'.join([prefix, name])
            else:
                prefixed_name = name
            return _import_by_name(prefixed_name)
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
#--- Creating 'phantom' modules from an XML description
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
            if inspect.isclass(object_cache[parent]):
                obj.__get__ = lambda: None
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


#------------------------------------------------------------------------------
#--- Manglers
#------------------------------------------------------------------------------

def mangle_docstrings(app, what, name, obj, options, lines,
                      reference_offset=[0]):
    cfg = app.config
    if what == 'class':
        doc = SphinxClassDoc(obj, role='', #func_doc=SphinxFunctionDoc,
                             block_format=cfg.numpydoc_default_block_type,
                             list_format=cfg.numpydoc_default_list_type)
        lines[:] = doc.format()
    elif what in ('function', 'method'):
        doc = SphinxFunctionDoc(obj, role='',
                                block_format=cfg.numpydoc_default_block_type,
                                list_format=cfg.numpydoc_default_list_type)
        docstring = doc.parse()
        docstring['Signature'] = []
        lines[:] = docstring.format()
    elif what == 'module':
        pass
    else:
        doc = SphinxDocString(obj.__doc__,
                              block_format=cfg.numpydoc_default_block_type,
                              list_format=cfg.numpydoc_default_list_type)
        lines[:] = doc.format()

    if app.config.numpydoc_edit_link and getattr(obj, '__name__', ''):
        v = dict(full_name=obj.__name__)
        lines += [''] + (app.config.numpydoc_edit_link % v).split('\n')
    # replace reference numbers so that there are no duplicates
    references = []
    for l in lines:
        l = l.strip()
        if l.startswith('.. ['):
            try:
                references.append(int(l[len('.. ['):l.index(']')]))
            except ValueError:
                print "WARNING: invalid reference in %s docstring" % name
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
    return

def mangle_signature(app, what, name, obj, options, args, retann):
    if args is not None:
        return (args, '')
    #
    # Do not try to inspect classes that don't define `__init__`
    if inspect.isclass(obj) and obj.__init__.__doc__ and \
       ('initializes x; see ' in obj.__init__.__doc__):
        return ('', '')
    #
    if not (callable(obj) or hasattr(obj, '__argspec_is_invalid_')):
        return (None, None)
    #
    obj_doc = getattr(obj, '__doc__', None)
    if not obj_doc:
        return (None, None)
    #
    args = NumpyDocString(obj_doc).extract_signature()
    if args is None:
        if inspect.isclass(obj):
            args = SphinxClassDoc(obj)._get_signature()
        elif inspect.isfunction(obj) or inspect.ismethod(obj):
            args = SphinxFunctionDoc(obj)._get_signature()
    return (args, '')


#------------------------------------------------------------------------------
#--- Monkeypatch sphinx.ext.autodoc to accept argspecless autodocs (old Sphinxes)
#------------------------------------------------------------------------------

def monkeypatch_sphinx_ext_autodoc():
    global _original_format_signature
    #
    if autodoc.RstGenerator.format_signature is our_format_signature:
        return
    #
    print "[numpydoc] Monkeypatching sphinx.ext.autodoc ..."
    _original_format_signature = autodoc.RstGenerator.format_signature
    autodoc.RstGenerator.format_signature = our_format_signature

def our_format_signature(self, what, obj, args, retann):
    (args, retann) = mangle_signature(None, what, None, obj, None, None, None)
    if args is not None:
        return args
    else:
        return _original_format_signature(self, what, obj, args, retann)


def initialize(app):
    try:
        app.connect('autodoc-process-signature', mangle_signature)
    except:
        monkeypatch_sphinx_ext_autodoc()
    
    fn = app.config.numpydoc_phantom_import_file
    if (fn and os.path.isfile(fn)):
        print "[numpydoc] Phantom importing modules from", fn, "..."
        import_phantom_module(fn)

def setup(app):
    #
    autodoc.setup(app)
    # Directives options ..................................
    fnc_options = {'module':directives.unchanged,
                   'noindex': directives.flag,}
    mod_options = {'members': autodoc.members_option,
                   'undoc-members': directives.flag,
                   'noindex': directives.flag,
                   'platform': lambda x: x,
                   'synopsis': lambda x: x,
                   'deprecated': directives.flag}
    cls_options = {'members': autodoc.members_option, 
                   'undoc-members': directives.flag,
                   'noindex': directives.flag, 
                   'inherited-members': directives.flag,
                   'show-inheritance': directives.flag}
    # Register basic directives ...........................
    app.add_directive('numpyfunction',
                      numpyfunction_directive,
                      1, (1,0,1), **fnc_options)
    app.add_directive('numpyclass',
                      numpyclass_directive,
                      1, (1,0,1), **cls_options)
    app.add_directive('numpymethod',
                      numpyfunction_directive,
                      1, (1,0,1), **fnc_options)
    app.add_directive('numpystaticmethod', 
                      numpyfunction_directive, 
                      1, (1,0,1), **fnc_options)
    app.add_directive('numpyexception',
                      numpyfunction_directive,
                      1, (1,0,1), **fnc_options)
    #
    app.connect('autodoc-process-docstring', mangle_docstrings)
    app.connect('builder-inited', initialize)
    app.add_config_value('numpydoc_phantom_import_file', None, True)
    app.add_config_value('numpydoc_edit_link', None, True)
    app.add_config_value('numpydoc_default_block_type', None, True)
    app.add_config_value('numpydoc_default_list_type', "field", True)

    app.add_directive('autosummary', autosummary_directive, 1, (0, 0, False))
