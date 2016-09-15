
import markdown
from sphinx.parsers import Parser


class BlockParser(markdown.blockparser.BlockParser):
    """ Parse Markdown blocks into a document object

    A wrapper class that stitches the various BlockProcessors together,
    looping through them and creating an ElementTree object.
    """
    def __init__(self, markdown, document):
        markdown.blockparser.BlockParser.__init__(self, markdown)
        self.root = document

    def parseDocument(self, lines):
        self.parseChunk(self.root, '\n'.join(lines))
        return self.root

    def warn(self, message, location=None):
        self.markdown.warn(message, location)


class _Markdown(markdown.Markdown):
    def __init__(self, parent_parser, *args, **kwargs):
        self.parent_parser = parent_parser
        markdown.Markdown.__init__(self, *args, **kwargs)

    def parse_document(self, source, document):
        """Read ``source`` into a docutils document

        Parameters
        ----------
        source : str
        document : docutils.nodes.document
        """
        if not source.strip():
            return

        source = str(source)
        self.lines = source.splitlines()

        for prep in self.preprocessors.values():
            self.lines = prep.run(self.lines)

        # Parse the high-level elements.
        root = self.parser.parseDocument(self.lines).getroot()

        # Run the tree-processors
        for treeprocessor in self.treeprocessors.values():
            newRoot = treeprocessor.run(root)
            if newRoot is not None:
                root = newRoot

        # Serialize _properly_.  Strip top-level tags.
        output = self.serializer(root)
        if self.stripTopLevelTags:
            try:
                start = output.index(
                    '<%s>' % self.doc_tag) + len(self.doc_tag) + 2
                end = output.rindex('</%s>' % self.doc_tag)
                output = output[start:end].strip()
            except ValueError:  # pragma: no cover
                if output.strip().endswith('<%s />' % self.doc_tag):
                    # We have an empty document
                    output = ''
                else:
                    # We have a serious problem
                    raise ValueError('Markdown failed to strip top-level '
                                     'tags. Document=%r' % output.strip())

        # Run the text post-processors
        for pp in self.postprocessors.values():
            output = pp.run(output)

        return output.strip()

    def warn(self, message, location=None):
        self.parent_parser.warn(message, location)


class MarkdownParser(Parser):
    supported = ('markdown', 'md')

    def parse(self, inputstring, document):
        self.setup_parse(inputstring, document)
        _Markdown().parse_document(inputstring, document)
        self.finish_parse()
