import json
import sys
import requests
from queue import Queue
import threading
import time
from collections import defaultdict
import logging
from bs4 import BeautifulSoup
import html
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class RSSFeedProcessor:
    def __init__(self):
        self.data = []
        self.queues = defaultdict(Queue)
        self.processed_data = []
        self.lock = threading.Lock()

    def read_from_stdin(self):
        for line in sys.stdin:
            try:
                item = json.loads(line.strip())
                self.data.append(item)
            except json.JSONDecodeError:
                logging.error(f"Invalid JSON: {line.strip()}")

    def get_article(self, link_field="link", groupby="source", output="html_content"):
        for item in self.data:
            group = item.get(groupby, "default")
            self.queues[group].put((item, link_field, output))

        threads = []
        for group, queue in self.queues.items():
            thread = threading.Thread(target=self.process_queue, args=(queue,))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

    def process_queue(self, queue):
        while not queue.empty():
            item, link_field, output = queue.get()
            self.fetch_and_store(item, link_field, output)
            queue.task_done()

    def ps(self, doc: str) -> str:
        """Return the text content of paragraph html tags"""
        soup = BeautifulSoup(doc, "html.parser")
        paragraphs = soup.find_all("p")
        result = []
        for p in paragraphs:
            # Replace HTML entities with UTF-8 entities
            text = html.unescape(str(p))
            # Remove any remaining HTML tags
            text = BeautifulSoup(text, "html.parser").get_text()
            result.append(text)
        return " ".join(result)

    def html2txt(self, htmlstr: str) -> str:
        """Convert HTML to plain text"""
        # Replace HTML entities with their UTF-8 counterparts
        utf8_string = html.unescape(htmlstr)
        # Remove remaining HTML markup
        utf8_string = re.sub("\n", "", utf8_string)
        return re.sub("<[^<]+?>", "", utf8_string)

    def fetch_and_store(self, item, link_field, output):
        url = item.get(link_field)
        if not url:
            item[output] = "Error: No URL found"
            logging.warning(f"No URL found for item: {item.get('title', 'Unknown title')}")
        else:
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                item[output] = response.text
                logging.info(f"Successfully fetched content for: {item.get('title', 'Unknown title')}")
            except requests.RequestException as e:
                item[output] = f"Error: {str(e)}"
                logging.error(f"Failed to fetch content for {url}: {str(e)}")

        with self.lock:
            self.processed_data.append(item)

    def output_data(self):
        for item in self.processed_data:
            json.dump(item, sys.stdout, ensure_ascii=False)
            sys.stdout.write('\n')
            sys.stdout.flush()

if __name__ == "__main__":
    processor = RSSFeedProcessor()
    processor.read_from_stdin()
    processor.get_article()
    processor.output_data()