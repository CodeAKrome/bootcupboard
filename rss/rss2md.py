#!/usr/bin/env python
import feedparser
import sys
import subprocess
from datetime import datetime
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text
from rich import box

console = Console()

def imgcat(url: str):
    """Display image inline using imgcat -u <url>"""
    try:
        # Run imgcat without redirecting stdout/stderr so it can print escape sequences to terminal
        result = subprocess.run(["imgcat", "-u", url], check=True, capture_output=False)
    except FileNotFoundError:
        console.print(f"[dim]imgcat not found – skipping inline image: {url}[/]")
    except subprocess.CalledProcessError as e:
        console.print(f"[dim]Failed to display image with imgcat: {url} (error: {e})[/]")
    except Exception as e:
        console.print(f"[dim]Unexpected error displaying image: {url} ({e})[/]")

def parse_date(date_input):
    """Safely parse date from string or struct_time, return readable string or raw if failed"""
    if not date_input:
        return "Unknown date"
    
    if hasattr(date_input, 'tm_year'):
        try:
            dt = datetime(*date_input[:6])
            return dt.strftime("%B %d, %Y at %H:%M")
        except:
            return "Invalid parsed date"
    
    if isinstance(date_input, str):
        date_str = date_input.strip()
        try:
            dt = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %z")
            return dt.strftime("%B %d, %Y at %H:%M")
        except ValueError:
            try:
                dt = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %Z")
                return dt.strftime("%B %d, %Y at %H:%M")
            except ValueError:
                return date_str

    return "Unknown date"

def extract_image_urls(entry):
    """Extract all possible image URLs from an entry"""
    images = set()
    
    if "enclosures" in entry:
        for enc in entry.enclosures:
            if enc.get("type", "").startswith("image/") and "url" in enc:
                images.add(enc["url"])
    
    if "media_content" in entry:
        for m in entry.media_content:
            if (m.get("medium") == "image" or m.get("type", "").startswith("image/")) and "url" in m:
                images.add(m["url"])
    
    if "media_thumbnail" in entry:
        for t in entry.media_thumbnail:
            if "url" in t:
                images.add(t["url"])
    
    if "links" in entry:
        for link in entry.links:
            if link.get("rel") == "enclosure" and link.get("type", "").startswith("image/") and "href" in link:
                images.add(link["href"])
    
    import re
    content = entry.get("summary", "") + entry.get("description", "") + "".join([c.get("value", "") for c in entry.get("content", [])])
    img_srcs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', content, re.IGNORECASE)
    for src in img_srcs:
        if src.startswith("http"):
            images.add(src)
    
    return list(images)

if len(sys.argv) < 2:
    console.print("[bold red]Usage:[/] python rss_with_imgcat.py <feed_url>")
    sys.exit(1)

url = sys.argv[1]
console.print(f"[dim]Fetching feed:[/] {url}\n")

feed = feedparser.parse(url)

if feed.bozo and feed.bozo_exception:
    console.print("[bold yellow]Warning:[/] Feed parsing issues:")
    console.print(f"{feed.bozo_exception}\n")

# Feed header
feed_info = feed.get("feed", {})
title = feed_info.get("title", "Untitled Feed")
description = feed_info.get("subtitle") or feed_info.get("description", "")
link = feed_info.get("link", "")
updated = parse_date(feed_info.get("updated") or feed_info.get("updated_parsed"))

header_text = Text()
header_text.append(title + "\n", style="bold bright_cyan underline")
if description:
    header_text.append(description + "\n\n", style="italic dim")
header_text.append(f"Updated: {updated}", style="dim")
if link:
    header_text.append(f"\nSource: {link}", style="link " + link)

console.print(Panel(header_text, title="RSS / Atom Feed", border_style="bright_blue", box=box.ROUNDED, padding=(1, 2)))
console.print()

console.print(f"[bold bright_white]Articles ({len(feed.entries)})[/]\n")

for idx, entry in enumerate(feed.entries, 1):
    entry_title = entry.get("title", "No title").strip()
    entry_link = entry.get("link", "").strip()
    pub_date = parse_date(entry.get("published") or entry.get("updated") or entry.get("published_parsed") or entry.get("updated_parsed"))
    author = entry.get("author", "Unknown author")
    
    categories = []
    if "tags" in entry:
        categories = [tag.get("term", "") for tag in entry["tags"]]
    elif "category" in entry:
        if isinstance(entry["category"], list):
            categories = entry["category"]
        else:
            categories = [entry["category"]]
    category_str = " • ".join([c for c in categories if c]) if categories else "Uncategorized"
    
    summary = entry.get("summary") or entry.get("description") or "No summary available"
    
    title_text = Text()
    title_text.append(f"{idx}. ", style="bold bright_yellow")
    if entry_link:
        title_text.append(entry_title, style="bold white link " + entry_link)
    else:
        title_text.append(entry_title, style="bold white")
    
    subtitle_text = Text()
    subtitle_text.append(f"{category_str}", style="bright_magenta")
    subtitle_text.append(f" • By {author} • {pub_date}", style="dim")
    
    console.print(Panel(
        Markdown(summary),
        title=title_text,
        subtitle=subtitle_text,
        border_style="bright_green",
        padding=(1, 2),
        expand=False
    ))
    
    images = extract_image_urls(entry)
    if images:
        console.print("[bold bright_magenta]Images in this article:[/]")
        for img_url in images:
            console.print(f"   → {img_url}")
            imgcat(img_url)
        console.print()
    
    console.print()  # spacing
