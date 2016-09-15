
import re

import docutils.nodes
import markdown


class NodeProcessor(markdown.blockprocessors.BlockProcessor):
    expr = r'^$'

    def test(self, parent, block):
        return bool(re.search(self.expr.format(tab=' '*self.tab_length), block))

    def run(self, parent, blocks):
        raise NotImplementedError()

    def warn(self, message, location=None):
        self.parser.warn(message, location)


class ListItemProcessor(markdown.blockprocessors.ListIndentProcessor):
    def create_item(self, parent, block):
        item = docutils.nodes.list_item()
        parent += item
        self.parser.parseBlocks(item, [block])


class LiteralBlockProcessor(NodeProcessor):
    expr = '^{tab}'
    node_type = docutils.nodes.literal_block

    def run(self, parent, blocks):
        previous = self.lastChild(parent)
        block = blocks.pop(0)
        rest = ''
        if isinstance(previous, self.node_type):
            # Continue previous block
            code = previous[0]
            block, rest = self.detab(block)
            previous[0] = docutils.nodes.Text('{}\n{}\n'.format(previous[0], block.rstrip()))
        else:
            # New literal block
            block, rest = self.detab(block)
            parent += self.node_type(text=block.rstrip())
        if rest:
            context = rest.splitlines()[0]
            if block:
                context = '\n    {}\n{}'.format(block.splitlines()[-1], context)
            self.warn('No blank line found after block', context)
            blocks.insert(0, rest)


class BlockQuoteProcessor(LiteralBlockProcessor):
    node_type = docutils.nodes.block_quote

    def test(self, parent, block):
        return bool(re.search('(^|\\n) {{0,{tablen1}}}>'.format(tablen1=self.tab_length-1), block))

    def detab(self, block):
        newblock = []
        rest = []
        for line in block.splitlines():
            if line.lstrip().startswith('>'):
                newblock.append(line.split('>', 1)[1])
            else:
                rest.append(line)
        return '\n'.join(newblock), '\n'.join(rest)
