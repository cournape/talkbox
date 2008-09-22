import inspect
import re
from warnings import warn

from docutils.statemachine import StringList

import sphinx.ext.autodoc as autodoc


#--- Defaults -----------------------------------------------------------------
# Define some defaults. Ideally, a user should be able to change them by setting
# some options in conf.py.

# How to format the name of a variable in a list
default_name_format = "**%s**"
# How to format the type of a variable in a list
default_type_format = "*%s*"
# How should we format the blocks ?
default_block_format = None
# How should we format list/descriptoins ?
default_list_format = "field"


#--- Regular expressions ------------------------------------------------------
empty_rgx = re.compile(r"^\s*$")
arguments_rgx = re.compile(r"^([a-zA-Z]\w*)(=\w+)?$")
pysig_rgx = re.compile(r"""(?P<parent>[a-zA-Z]\w*[.])?
                           (?P<name>[a-zA-Z]\w*)\s*
                           \((?P<args>.*)\)\s*
                           (\s* -> \s* .*)?
                        """, re.VERBOSE)
directive_rgx = re.compile(r'''^\s*              # Some indentation
                               [.]{2}            # ..
                               \s(?P<desc>\w+)   # directive name
                               ::\s*             # ::
                               (?P<arg>\w.+)*$   # directive argument
                            ''', re.VERBOSE)
description_rgx = re.compile('^(?P<name>\w+[^:]*)(?:\s+:\s+(?P<type>.*))?$')
doctest_rgx = re.compile(r'>>>( +|$)')
field_rgx = re.compile(r"\s*:(?P<name>\w+):\s*(?P<args>.+)?")

# Synonyms
synonyms = {'attribute': 'Attributes',
            'attributes': 'Attributes',
            #
            'describe': 'describe',
            #
            'example': 'Examples',
            'examples': 'Examples',
            #
            'index': 'index',
            #
            'note': 'Notes',
            'notes': 'Notes',
            #
            'other parameter': 'Other Parameters',
            'other parameters': 'Other Parameters',
            #
            'parameter': 'Parameters',
            'parameters': 'Parameters',
            #
            'raise': 'Raises',
            'raises': 'Raises',
            #
            'reference': 'References',
            'references': 'References',
            #
            'return': 'Returns',
            'returns': 'Returns',
            #
            'see also': 'See Also',
            'seealso': 'See Also', 
            #
            'summary':'Summary',
            'extended summary': 'Extended Summary',
            #
            'warn': 'Warns',
            'warns': 'Warns',
            #
            'warning': 'Warnings',
            'warnings': 'Warnings',
            }


#--- Builders -----------------------------------------------------------------

class BlockFormatter(object):
    """Defines a class of functions to format sections (blocks).
    An instance is initialized by giving a type of output (`block_type`) and
    optionally a delimitor.
    The instance can then be called with a header and some contents.
    
    :Attributes:
       **block_type** : {'topic','rubric','describe','field','section'}, string
           Output type for a block. For example, 'section' will output each block
           as a separate section, while 'field' will output the block as a list
           of fields...
        **delimitor**: {'~'}, string
           Character used for the delimitation of the header and the content for
           a section.
    
    """
    #
    def __init__(self, block_type, delimitor='~'):
        if block_type == 'topic':
            formatstr = "\n\n.. topic:: %s\n"
            tab = 0
        elif block_type == 'rubric':
            formatstr = "\n\n.. rubric:: %s\n\n"
            tab = 0
        elif block_type == 'describe':
            formatstr = "\n\n.. describe:: %s\n\n\n"
            tab = 3
        elif block_type == 'field':
            formatstr = "\n\n:%s:\n\n"
            tab = 3
        elif block_type == 'section':
            formatstr = "\n\n%s\n%s\n\n"
            tab = 0
        else:
            formatstr = "**%s**:\n\n\n"
            tab = 3
        self.format_string = formatstr
        self.tab = tab
        self.delim = delimitor
    #
    def __call__(self, header, content):
        try:
            output = Docstring(self.format_string % header)
        except TypeError:
            output = Docstring(self.format_string % (header,
                                                     self.delim * len(header)))
        output += Docstring(content).indent(self.tab)
        return output

#---  Generic functions -------------------------------------------------------


class Docstring(list):
    """A subclass of the standard Python list, with some improved functionalities.
    Basically, this class is a simpler version of ``docutils.StringList``, without
    parent tracking.
    
    """
    #
    def __init__(self, text):
        #
        # Skip the pre-processing if we already have a Docstring
        if isinstance(text, Docstring):
            rawdoc = text
        # Use autodoc.prepare_docstring on strings
        elif isinstance(text, basestring):
            rawdoc = autodoc.prepare_docstring(text)
            # Careful: prepare_docstring adds an extra blank line...
            rawdoc.pop(-1)
        # A StringList or a list: make sure that we don't start with empty lines
        elif isinstance(text, (list, StringList)):
            rawdoc = text
            while rawdoc and not rawdoc[0]:
                rawdoc.pop(0)
        #
        list.__init__(self, rawdoc)
    #
    def __str__(self):
        return "\n".join(self)
    #
    def __getslice__(self, start, end):
        # When slicing a Docstring, we must get a Docstring 
        return Docstring(list.__getslice__(self, start, end))
    #    
    def first_non_empty(self, start=0):
        """Finds the first non empty line after the line `start` (included).
        
        """
        i = start
        while (i < len(self)-1) and empty_rgx.match(self[i]):
            i += 1
        return self[i]
    #
    def deindent(self, n=None, start=0, end=None):
        """
        Removes the first `n` spaces from the beginning of each line between
        `start` and `end`.
        
        :param n: Number of spaces to remove. If ``None``, defaults to the number
                  of spaces of the first non-empty line.
        """
        # Get the nb of empty spaces to fill
        if n is None:
            first = self.first_non_empty(start)
            n = len(first) - len(first.lstrip())
        # Get the target
        if end is None:
            target = slice(start, end)
        else:
            target = slice(start, end+1)
        # Now, get rid of the leading spaces in target (if possible)
        for (i,line) in enumerate(self[target]):
            if line[:n] == ' '*n:
                self[i+start] = line[n:]
        return self
    #
    def indent(self, n=0, start=0, end=None):
        """
    Adds `n` spaces at the beginning of each line, **in place**.
    
    :Parameters:
        **n** : int, optional
            Number of space to add.
        **start** : int, optional
            Index of the first line to process
        **end** : {None, int}, optional
            Index of the last line to process
        """
        if n:
            if end is None:
                target = slice(start, end)
            else:
                target = slice(start, end+1)
            self[target] = [' '*n + line for line in self[target]]
        return self
    #
    def is_at_section(self, idx):
        """
    Returns True if a section starts at line `idx`.

        """
        try:
            current_line = self[idx]
        except IndexError:
            return False
        #
        if not current_line.strip() or (idx == len(self)-1):
            return False
        #
        next_line = self[idx+1]
        if not next_line.strip():
            return False
        elif (len(next_line) == len(current_line)) and\
            set(next_line).issubset('"-_~`'):
            return True
        return False
    #
    def is_at_directive(self, idx):
        """
    Returns True if a directive is detected at line `idx`.

        """
        #
        try:
            match = directive_rgx.match(self[idx])
        except IndexError:
            return
        else:
            if match and match.group('desc') not in ['math']:
                return match
        return
    #
    def get_indented(self, start=0, until_blank=0, strip_indent=1,
                     block_indent=None, first_indent=None):
        """
    Extract and return a Docstring of indented lines of text.

    Collect all lines with indentation, determine the minimum indentation,
    remove the minimum indentation from all indented lines (unless `strip_indent`
    is false), and return them. All lines up to but not including the first
    unindented line will be returned.

    :Parameters:
      - `start`: The index of the first line to examine.
      - `until_blank`: Stop collecting at the first blank line if true.
      - `strip_indent`: Strip common leading indent if true (default).
      - `block_indent`: The indent of the entire block, if known.
      - `first_indent`: The indent of the first line, if known.

    :Return:
      - a StringList of indented lines with mininum indent removed;
      - the amount of the indent;
      - a boolean: did the indented block finish with a blank line or EOF?

    .. note::

       This method is nothing but ``docutils.statemachine.StringList.get_indented``
        """
        indent = block_indent           # start with None if unknown
        end = start
        if block_indent is not None and first_indent is None:
            first_indent = block_indent
        if first_indent is not None:
            end += 1
        last = len(self)
        while end < last:
            line = self[end]
            if line and (line[0] != ' '
                         or (block_indent is not None
                             and line[:block_indent].strip())):
                # Line not indented or insufficiently indented.
                # Block finished properly iff the last indented line blank:
                blank_finish = ((end > start) and not self[end-1].strip())
                break
            stripped = line.lstrip()
            if not stripped:            # blank line
                if until_blank:
                    blank_finish = 1
                    break
            elif block_indent is None:
                line_indent = len(line) - len(stripped)
                if indent is None:
                    indent = line_indent
                else:
                    indent = min(indent, line_indent)
            end += 1
        else:
            blank_finish = 1            # block ends at end of lines
        block = self[start:end]
        if first_indent is not None and block:
            block[0] = block[0][first_indent:]
        if indent and strip_indent:
            block.deindent(indent, start=(first_indent is not None))
        return (block, indent) or (0, blank_finish)


    def get_paragraphs(self):
        """Returns a list of contiguous blocks."""
        blocks = []
        i = 0
        while i < len(self):
            j = i
            current_block = []
            line = self[j]
            while line and (j < len(self)-1):
                current_block += [line]
                j += 1
                line = self[j]
            blocks.append(current_block)
            i = j+1
        return blocks

    def paragraphs_as_list(self):
        """Transforms a list of paragraphs as a rst list."""
        #
        blocks = self.get_paragraphs()
        lines = []
        for block in blocks:
            if not block:
                lines.append('')
            else:
                lines.append('* ' + block[0])
                lines += ['  ' + line for line in block[1:]]
        self[:] = lines[:]
        return self

#------------------------------------------------------------------------------


class NumpyDocString(Docstring):
    """
    
    """
    #
    name_format = default_name_format
    type_format = default_type_format
    default_block_format = default_block_format
    default_list_format = default_list_format
    #
    def __init__(self, docstring,
                 block_format=None, list_format=None, role=''):
        # Remove the indentation, starting on the second line
        Docstring.__init__(self, docstring)
        self.deindent()
        self.section = {'Signature': [],
                        'Summary': '',
                        'Extended Summary': [],
                        'Parameters': [],
                        'Returns': [],
                        'Raises': [],
                        'Warns': [],
                        'Warnings': [],
                        'Other Parameters': [],
                        'Attributes': [],
                        'Methods': [],
                        'See Also': [],
                        'Notes': [],
                        'References': '',
                        'Examples': '',
                        'index': {}
                         }
        #
        self._parsed = False
        self.section_slices = None
        #
        if block_format is None:
            block_format = self.default_block_format
        if list_format is None:
            list_format = self.default_list_format
        self.block_formatter = BlockFormatter(block_format)
        self.list_formatter = BlockFormatter(list_format)
        self._role = role


    def __getitem__(self, item):
        if isinstance(item, basestring):
            return self.section[item]
        #print "NUmpyDocString[%s]:%s" % (item, '\n'.join(self))
        try:
            return Docstring.__getitem__(self, item)
        except IndexError:
            return ''

    def __setitem__(self, item, value):
        if isinstance(item, basestring):
            self.section[item] = value
        else:
            Docstring.__setitem__(self, item, value)

    def __delitem__(self, item):
        if isinstance(item, basestring):
            del self.section[item]
        else:
            Docstring.__delitem__(self, item)


    def extract_signature(self):
        """
    If the first line of the docstring is a signature followed by an empty line,
    remove the first two lines from the docstring and return the argument list.
    If no signature is found, return the docstring as is and None as the
    argument list.
    
    :param docstring: A StringList object containing the docstring.
    :return: (docstring, argument list)
        """
        sig = pysig_rgx.match(self[0].strip())
        empty = (len(self) == 1) or (self[1].strip() == '')
        
        # Now check if the arguments are valid.
        if sig and empty:
            # Get the arguments
            args = sig.group('args')
            # Remove the spaces
            arglist = [a.strip() for a in args.split(',')]
            # Validate the regex
            valid_args = [a for a in arglist if arguments_rgx.match(a)]
            # Print valid_args
            if arglist == [''] or (arglist == valid_args):
                self['Signature'] = sig.group()
                del self[:2]
                return "(%s)" % ', '.join(arglist)
        return ''


    def parse(self):
        #
        self.extract_signature()
        self.deindent()
        #
        sectidx = {}
        sectidx['Summary'] = contentidx = [0, 0]
        i = 0
        while (i < len(self)):
            if self.is_at_section(i):
                key = self[i].lower()
                try:
                    header = synonyms[key]
                except KeyError:
                    warn("Unknown section %s" % key)
                i += 2
                sectidx[header] = contentidx = [i, i]
                continue
            match = self.is_at_directive(i)
            if match:
                header = synonyms[match.group('desc').lower()]
                args = match.group('arg')
                self.insert(i+1, args or ' ')
                sectidx[header] = contentidx = [i+1, i+1]
            else:
                contentidx[-1] += 1
            i += 1
        #
        self.section_slices = dict([(h, slice(s[0],s[1]))
                                    for (h,s) in sectidx.iteritems()])
        self.section.update([(h, self[s[0]:s[1]])
                             for (h,s) in sectidx.iteritems()])
        #
        for header in ['Parameters', 'Returns', 'Raises', 'Warns']:
            self._fix_description(header)
        self._fix_examples()
        self._fix_see_also()
        self._fix_notes()
        self._fix_references()
        self._parsed = True
        return self


    def _split_description(self, header):
        #
        if (header not in self.section) or (not self.section[header]):
            return []
        #
        contents = self[header]
        output = []
        i = 0
        while i < len(contents):
            line = contents[i]
            match = description_rgx.match(line.rstrip())
            if match:
                (v_name, v_type) = match.groups()
                (desc, _) = contents.get_indented(start=i+1, until_blank=True)
                output.append((v_name, v_type, desc))
                i += len(desc)
            else:
                i+=1
        return output


    def _fix_description(self, header):
        #
        if (header not in self.section) or (not self.section[header]):
            return []
        #
        contents = self.section[header]
        output = []
        i = 0
        while i < len(contents):
            line = contents[i]
            match = description_rgx.match(line.rstrip())
            if match:
                (v_name, v_type) = match.groups()
                output.append('')
                if v_type:
                    output.append("%s : %s" % (self.name_format % v_name, 
                                               self.type_format % v_type))
                else:
                    output.append("%s" % (self.name_format % v_name))
                (desc, _) = contents.get_indented(start=i+1, 
                                                  until_blank=True)
                output += desc.indent(3)
                # If desc == [] we still need to increment.
                i += len(desc) or 1
            else:
                i +=1
        output.append('')
        if output != ['']:
            contents[:] = output
        return output


    def _fix_examples(self):
        #
        def opened_quote(text):
            odd_single = (len(text.split("'")) % 2)
            odd_double = (len(text.split('"')) % 2)
            return not (odd_single and odd_double)
        #
        if not self['Examples']:
            return []
        contents = self['Examples']
        contents.insert(0,'')
        (i, ilast) = (0, len(contents))
        while i < ilast:
            line = contents[i]
            if doctest_rgx.match(line) and opened_quote(line):
                j = i+1
                while j < ilast:
                    next_line = contents[j]
                    if next_line == '':
                        contents[i] += "\\n"
                        ilast -= 1
                        del contents[j]
                    elif opened_quote(next_line):
                        contents[i] += "\\n" + next_line
                        ilast -= 1
                        del contents[j]
                        break
                    else:
                        j += 1
            i += 1
        return contents


    def _fix_see_also(self):
        if not self.section['See Also']:
            return []
        #
        func_role = self._role
        functions = []
        current_func = None
        rest = Docstring([])
        for line in self.section['See Also']:
            if not line.strip(): continue
            if ':' in line:
                if current_func:
                    functions.append((current_func, rest))
                r = line.split(':', 1)
                current_func = r[0].strip()
                r[1] = r[1].strip()
                if r[1]:
                    rest = Docstring([r[1]])
                else:
                    rest = Docstring([])
            elif not line.startswith(' '):
                if current_func:
                    functions.append((current_func, rest))
                    current_func = None
                    rest = Docstring([])
                if ',' in line:
                    for func in line.split(','):
                        func = func.strip()
                        if func:
                            functions.append((func, []))
                elif line.strip():
                    current_func = line.strip()
            elif current_func is not None:
                rest.append(line.strip())
        if current_func:
            functions.append((current_func, rest))
        #
        output = []
        last_had_desc = True
        for (func, desc) in functions:
            if func_role:
                link = ":%s:`%s`" % (func_role, func)
            else:
                link = "`%s`_" % func
            if desc or last_had_desc:
                output += ['']
                output += [link]
            else:
                output[-1] += ", %s" % link
            if desc:
                output += desc.indent(4)
                last_had_desc = True
            else:
                last_had_desc = False
        output += ['']
        self['See Also'][:] = output
        return output


    def _fix_references(self):
        pass


    def _fix_notes(self):
        if self['Notes'] and self['Notes'][0] != '':
            self['Notes'].insert(0,'')


    def _split_index(self):
        """
        .. index: default
           :refguide: something, else, and more

        """
        def strip_each_in(lst):
            return [s.strip() for s in lst]
        #
        info = self['index']
        if not info:
            return {}
        #
        (section, content) = (info[0], info[1:])
        out = {}
        out['default'] = strip_each_in(section.strip().split(','))[0]
        for line in content:
            match = field_rgx.match(line)
            if match:
                (name, args) = match.groups()
                out[name] = strip_each_in((args or '').split(','))
        return out

    def _format_block(self, header):
        if self[header]:
            return self.block_formatter(header, self[header])
        return []

    def _format_list(self, header):
        if self[header]:
            return self.list_formatter(header, self[header])
        return []

    def _format_signature(self):
        if self['Signature']:
            return [self['Signature'].replace('*','\*')] + ['']
        else:
            return ['']

    def _format_see_also(self):
        if not self['See Also']:
            return []
        return self.block_formatter('See Also', self['See Also'])

    def _format_index(self):
        idx = self._split_index()
        out = []
        out += ['.. index:: %s' % idx.get('default','')]
        for section, references in idx.iteritems():
            if section == 'default':
                continue
            out += ['   :%s: %s' % (section, ', '.join(references))]
        return out

    def _format_warnings(self):
        if self['Warnings']:
            return self._format_block('Warnings')
        return []

    def format(self):
        if not self._parsed:
            self.parse()
        section = self.section
        out = Docstring([])
        out += self._format_signature()
        #
        for header in ['Summary', 'Extended Summary']:
            if section[header]:
                out += section[header]
            if out[-1] != '':
                out += ['']
        #
        for header in ('Parameters','Returns','Raises', 'Warns'):
            out += self._format_list(header)
        #
        out += self._format_see_also() #("obj")
        out += self._format_block('Notes')
        out += self._format_warnings()
        out += self._format_block('References')
        out += self._format_block('Examples')
#        out = Docstring(out).indent(indent)
        return out

    def __str__(self):
        return '\n'.join(self.format())


class FunctionDoc(NumpyDocString):
    #
    default_block_format = default_block_format
    default_list_format = default_list_format
    #
    def __init__(self, func, role='func',
                 block_format=None, list_format=None):
        self._f = func
        try:
            NumpyDocString.__init__(self, inspect.getdoc(func) or '', 
                                    role=role,
                                    block_format=block_format,
                                    list_format=list_format)
        except ValueError, e:
            print '*'*78
            print "ERROR: '%s' while parsing `%s`" % (e, self._f)
            print '*'*78
            #print "Docstring follows:"
            #print doclines
            #print '='*78

    def _get_signature(self):
        try:
            # try to read signature
            argspec = inspect.getargspec(self._f)
            argspec = inspect.formatargspec(*argspec)
            argspec = argspec.replace('*','\*')
            signature = '%s%s' % (self._f.__name__, argspec)
        except TypeError:
            signature = '%s()' % self._f.__name__
        self['Signature'] = signature
        return signature

    def format(self):
        if not self._parsed:
            self.parse()


        out = []

        roles = {'func': 'function',
                 'meth': 'method'}
        if self._role:
            role = roles.get(self._role, '')
            if not role:
                print "Warning: invalid role %s" % self._role
            sig = self['Signature']
            if not self['Signature']:
                self['Signature'] = self._get_signature()
            if sig is None:
                out += ['.. %s:: %s' % (role, self._f.__name__), '']
            else:
                out += ['.. %s:: %s(%s)' % (role, self._f.__name__, sig), '']

        out += super(FunctionDoc, self).format().indent(3)

        return out


class ClassDoc(NumpyDocString):
    #
    default_block_format = default_block_format
    default_list_format = default_list_format
    #
    def __init__(self, cls, modulename='', func_doc=FunctionDoc,
                 block_format=None, list_format=None, role=''):
        if not inspect.isclass(cls):
            raise ValueError("Initialise using a class. Got %r" % cls)
        self._cls = cls

        if modulename and not modulename.endswith('.'):
            modulename += '.'
        self._mod = modulename
        self._name = cls.__name__
        self._func_doc = func_doc

        NumpyDocString.__init__(self, cls.__doc__, role=role,
                                block_format=block_format,
                                list_format=list_format)

    @property
    def methods(self):
        return [name for (name, func) in inspect.getmembers(self._cls)
                if not name.startswith('_') and callable(func)]

    def __str__(self):
        out = ''
        out += super(ClassDoc, self).__str__()
        out += "\n\n"
        return out


################################################################################

class SphinxDocString(NumpyDocString):

    default_block_format = default_block_format
    default_list_format = default_list_format
    
    def _fix_references(self):
        references = self['References']
        for (i,line) in enumerate(references):
            references[i] = re.sub('\[[0-9]+\]', '[#]', line)
        if references:
            references.append('')
        return

    def _format_signature(self):
        if self['Signature']:
            return ['``%s``' % self['Signature']] + ['']
        return ['']

    def _format_warnings(self):
        out = []
        if self['Warnings']:
            out = ['.. warning::']
            out += self['Warnings'].indent(3)
        return out

    def _format_see_also(self):
        out = []
        if self['See Also']:
            out = ['.. seealso::']
            out += self['See Also'].indent(3)
        return out
    
    def _format_index(self):
        idx = self._split_index()
        if not idx:
            return []
        
        out = []
        out += ['.. index:: %s' % idx.get('default','')]
        for section, references in idx.iteritems():
            if section == 'default':
                continue
            elif section == 'refguide':
                out += ['   single: %s' % (', '.join(references))]
            else:
                out += ['   %s: %s' % (section, ','.join(references))]
        return out


class SphinxFunctionDoc(SphinxDocString, FunctionDoc):
    default_block_format = default_block_format
    default_list_format = default_list_format


class SphinxClassDoc(SphinxDocString, ClassDoc):
    default_block_format = default_block_format
    default_list_format = default_list_format
    pass

################################################################################

if __name__ == '__main__':
    basetext = """
    A one-line summary that does not use variable names or the
    function name.

    Several sentences providing an extended description. Refer to
    variables using back-ticks, e.g. `var`.

    Parameters
    ----------
    var1 : array_like
        Array_like means all those objects -- lists, nested lists, etc. --
        that can be converted to an array.  We can also refer to
        variables like `var1`.
    var2 : int
        The type above can either refer to an actual Python type
        (e.g. ``int``), or describe the type of the variable in more
        detail, e.g. ``(N,) ndarray`` or ``array_like``.
    Long_variable_name : {'hi', 'ho'}, optional
        Choices in brackets, default first when optional.

    Returns
    -------
    describe : type
        Explanation
    output
        Explanation
    tuple
        Explanation
    items
        even more explaining

    Other Parameters
    ----------------
    only_seldom_used_keywords : type
        Explanation
    common_parameters_listed_above : type
        Explanation

    Raises
    ------
    BadException
        Because you shouldn't have done that.

    See Also
    --------
    otherfunc : relationship (optional)
    newfunc : Relationship (optional), which could be fairly long, in which
              case the line wraps here.
    thirdfunc, fourthfunc, fifthfunc

    Notes
    -----
    Notes about the implementation algorithm (if needed).

    This can have multiple paragraphs.

    You may include some math:

    .. math:: X(e^{j\omega } ) = x(n)e^{ - j\omega n}

    And even use a greek symbol like :math:`omega` inline.

    References
    ----------
    Cite the relevant literature, e.g. [1]_.  You may also cite these
    references in the notes section above.

    .. [1] O. McNoleg, "The integration of GIS, remote sensing,
       expert systems and adaptive co-kriging for environmental habitat
       modelling of the Highland Haggis using object-oriented, fuzzy-logic
       and neural-network techniques," Computers & Geosciences, vol. 22,
       pp. 585-588, 1996.

    Examples
    --------
    These are written in doctest format, and should illustrate how to
    use the function.

    >>> a=[1,2,3]
    >>> print [x + 3 for x in a]
    [4, 5, 6]
    >>> print "a\n\nb"
    a
    <BLANKLINE>
    b
    """
    doc = FunctionDoc(basetext)