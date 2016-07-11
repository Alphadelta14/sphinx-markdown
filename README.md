# sphinx-markdown
This provides Markdown file support for Sphinx via RST inclusion.

## Installation

```bash
pip install sphinx-markdown
```

## Using
Add `sphinx_markdown` to your Sphinx project's `conf.py` by appending it to the
`extensions` list.

### Configuration
There are a couple of configuration options available.

* `markdown_extensions` provides a list of extensions to be passed to the
    Markdown parser
* `markdown_search` replaces the search functionality to use the included
    Markdown document instead of just the filename. You will need to set
    `html_copy_source` to `True` in order for search to work.

### Example Config

```python

extensions = ['sphinx.ext.autodoc', 'numpydoc', 'sphinx_markdown']

html_copy_source = True

markdown_search = True
markdown_extensions = ['gfm']  # Github Flavored Markdown (pip install py-gfm)
```

### Example RST

```rst
.. markdown-ingest::
    filename: README.md
```
