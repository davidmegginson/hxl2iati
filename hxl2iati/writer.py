""" Simple XML writer with basic error checking

Usage:
  import hxl2iati.writer, sys

  xmlout = new XMLWriter(output=sys.stdout, indent_step=2)
  xmlout.start_document()
  xmlout.start_block("foo", {"xml:id": "12345"})
  xmlout.simple_element("bar", {"xml:lang": "en"}, "Here is some content &&& <<<")
  xmlout.end_block("foo")
  xmlout.end_document()

"""

import re, sys


class XMLException (Exception):
    """ Any type of XML well-formedness error.

    """

    def __init__ (self, message):
        """ Constructor
        Parameters:
          message the message to send with the exception

        """
        super().__init__(message)

        
class XMLWriter:
    """ XML-level writer for IATI data with basic well-formedness checks
    Does not handle mixed content (not needed for IATI).
    
    """

    def __init__ (self, output=None, indent_step=2, encoding=None):
        """ Constructor
        Parameters:
          output a Python file object (default: sys.stdout)
          indent_step the number of spaces to indent for each level in the XML document (default: 2)
          encoding the character encoding to list in the XML declaration (default is none)

        """
        self.output = output
        if self.output is None:
            self.output = sys.stdout
        self.indent_step = indent_step
        self.encoding = encoding

        # internal state
        self._stack = []
        self._in_document = False
        self._seen_element = False

    def start_document (self):
        """ Start an XML document
        Exception:
          XMLException if there is already a document open

        """
        if self._in_document:
            raise XMLException("XML document already in progress")
        if self.encoding is None:
            print("<?xml version=\"1.0\"?>\n", file=self.output)
        else: 
            print("<?xml version=\"1.0\" encoding=\"{}\"?>\n".format(esc(self.encoding)), file=self.output)
        self._in_document = True

    def end_document (self):
        """ Finish an XML document.
        Leaves the writer in a state where it can start a new one.
        Exception:
          XMLException if there is no document open, there was no root element, or an element is still open.

        """
        if not self._in_document:
            raise XMLException("No XML document started")
        if not self._seen_element:
            raise XMLException("No root element in document")
        if len(self._stack) > 0:
            raise XMLException("Unclosed elements: {}".format(", ".join(self._stack)))
        print("", file=self.output)
        self._in_document = False
        self._seen_element = False

    def start_block (self, name, atts={}):
        """ Start a block element, child elements will be indented
        Parameters:
          name the XML element name
          atts a dict of attribute names and values (defaults to {})
        Exception:
          XMLException if the parameters would not result in a well-formed XML document
        
        """
        self._check_element(name)
        print(self._indent + make_start_tag(name, atts))
        self._stack.append(name)

    def end_block (self, name):
        """ End a block element
        Parameters:
          name the XML element name (just for confirmation)
        Exception:
          XMLException if the parameters would not result in a well-formed XML document

        """
        if len(self._stack) == 0:
            raise XMLException("Root element already closed; no XML block to end with {}".format(name))
        old_name = self._stack.pop()
        if name != old_name:
            raise XMLException("Expected to end element {}, but found {}".format(old_name, name))
        print(self._indent + make_end_tag(name))

    def simple_element (self, name, atts={}, content=None):
        """ Display a simple element with only text content
        If the content is None, display an empty-element tag.
        Parameters:
          name the XML element name
          atts a dict of XML attribute names and values (default: {})
          content: text content of the element (default: None)
        """
        self._check_element(name)
        if content is None:
            print(self._indent + make_empty_tag(name, atts))
        else:
            print(self._indent + make_start_tag(name, atts) + esc(content) + make_end_tag(name))

    def _check_element (self, name):
        """ Check that an element is allowed in the current context.
        1. The document must be started
        2. It must not be an attempt at a second root element
        Marks that we've seen an element.
        Parameters:
          name the element name (for error reporting)
        Exception:
          XMLException if starting an element is not allowed in this context
        
        """
        
        if not self._in_document:
            raise XMLException("Attempt to add element {} before starting document".format(name))
        if len(self._stack) == 0 and self._seen_element:
            raise XMLException("There can be only one root element in an XML document: {}".format(name))
        self._seen_element = True

    @property
    def _indent (self):
        """ Return the indent string for the current stack level

        """
        return " " * self.indent_step * len(self._stack)


#
# Lexical helper functions for XML
#

def esc (s, is_attribute=False):
    """ escape XML special charcters 
    Parameters:
      is_attribute if True, also escape " and ' for attribute values
    Returns:
      the escaped string
    
    """
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    if is_attribute:
        return s.replace('"', "&quot;").replace("'", "&apos;")
    else:
        return s

def check_name (name):
    """ Check for a well-formed XML name
    Does not support XML namespaces
    Returns:
      the name provided, if it's well-formed
    Exception:
      XMLException if the name is not well-formed

    """
    if re.match(r"^(?:[a-zA-Z][a-zA-Z0-9_-]*:)?[a-zA-Z][a-zA-Z0-9_-]*$", name):
        return name
    else:
        raise XMLException("Malformed XML name: {}".format(name))

def make_att_str (atts):
    """ Make a string of attributes for a start tag 
    Parameters:
      atts a dict of attribute names and values
    Returns:
      an string of attributes in XML format, with a leading space
    Exception:
      XMLException if any of the attribute names is not well-formed

    """
    att_str = ""
    for name in atts:
        att_str = att_str + " {}=\"{}\"".format(check_name(name), esc(atts[name], True))
    return att_str

def make_start_tag (name, atts={}):
    """ Make an XML start tag, optionally with attributes
    Parameters:
      name the element name 
      atts a dict of attribute names and values
    Returns:
      the start tag as an XML string
    Exception:
      XMLException if the element name or any of the attribute names is not well-formed

    """
    return "<{}{}>".format(check_name(name), make_att_str(atts))

def make_end_tag (name):
    """ Make an XML end tag
    Parameters:
      name the element name
    Returns:
      the end tag as an XML string
    Exception:
      XMLException if the element name is not well-formed

    """
    return "</{}>".format(check_name(name))

def make_empty_tag (name, atts={}):
    """ Make an XML empty-element tag, optionally with attributes
    Parameters:
      name the element name 
      atts a dict of attribute names and values
    Returns:
      the empty-element tag as an XML string
    Exception:
      XMLException if the element name or any of the attribute names is not well-formed

    """
    return "<{}{}/>".format(check_name(name), make_att_str(atts))

# end
