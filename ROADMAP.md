# ROADMAP

## Required Functionality

### Represent README markdown as tree structure
Something like:
```
Node(section, body, children)
```
where section is something like `# header`, body is something like regular text/examples, etc under the heading, and children is an optional list of any nodes with sections with a number of `#` greater than the parent

### Function to serialize a README text file to tree structure
Something like:
```python
with open("README.md", "r") as f:
    readme = to_tree_structure(f)
```

### Function to take a Python module and, for each function/class/etc within, generate a tree structure
Something like:
```python
with open("module.py", "r") as f:
    output = module_to_trees(f)
```
NOTE: if we want relative links to appear in the section headings, we need a way to encode the heading in such a way that the two examples below are considered equal (and therefore, the latter should be used):

```#### Function [`fnc`](./path/to/module...)```<br>
```#### Function [`fnc`](./updated/path/to/module...)```

Essentially, we need to only compare what is visible from the non-raw view.

### Function to take a README tree and module trees and overwrite the README branches with branches from the module
This should recursively traverse the README graph and, at each node, check to see if the node section names match.
If they do, the function should replace that README node with the module node.
When the traversal is complete, a single tree object should be returned such that:
1. if the module had zero nodes, the tree output is the same as the tree input
1. if the module had >0 nodes, the tree is the same as the tree input BUT with the common nodes replaced by the module ones
1. if the README tree is null, the output tree is just the module graphs concatenated
1. if the module has a node that the README doesn't have, insert it in alphabetical order

There should be functionality to understand that if a function heading appears in the README but not the module graph, that it should be removed from the readme (or some kind of behavior that accounts for removed functions/classes/etc).