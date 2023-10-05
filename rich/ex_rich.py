from rich import print as rprint
from rich.console import Console
from rich.markdown import Markdown
from tqdm import trange, tqdm

MARKDOWN = """
# Sample
* a
* thing
---
"""

console = Console()
md = Markdown(MARKDOWN)
console.print(md)

rprint("[italic red]Hello[/italic red] World!", locals())

for i in trange(100):
    print(i)
