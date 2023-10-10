import curses
import chromadb
import sys

# Mocked Chroma database data
collections = ["Collection1", "Collection2", "Collection3"]
records = {
    "Collection1": ["Record1", "Record2", "Record3"],
    "Collection2": ["RecordA", "RecordB", "RecordC"],
    "Collection3": ["DataX", "DataY", "DataZ"],
}

records = {}
client = chromadb.PersistentClient(path=sys.argv[1])
colls = client.list_collections()
collections = [c.name for c in colls]
for collection in collections:
    records[collection] = []
    cc_handle = client.get_collection(collection)
    data = cc_handle.get()
    docs = data["documents"]
    meta = data["metadatas"]
    ids = data["ids"]
    for i, d, m in zip(ids, docs, meta):
        records[collection].append({"id":i,"doc":d,"meta":m})

def main(stdscr):
    curses.curs_set(0)  # Hide the cursor
    current_collection_index = 0
    current_record_index = 0

    # Initialize the color pair.
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    while True:
        stdscr.clear()

        # Get the current collection and its records
        current_collection = collections[current_collection_index]
        current_records = records[current_collection]

        # Display the current collection name at the top
#        stdscr.addstr(0, 0, f"Current Collection: {current_collection}")

        # Display the current collection name at the top of the page, highlighted in bold.
#        stdscr.addstr(0, 0, "Current collection: **{}**".format(current_collection.name), curses.A_BOLD)
        stdscr.addstr(0, 0, "Current collection: **{}**".format(current_collection), curses.color_pair(1))

        # --=={ Display the current record }==--
        current_record = current_records[current_record_index]

        stdscr.addstr(2, 0, f"{current_record['id']}")
        i = 3
        for k in current_record.keys():
            if k == "doc" or k =="id":
                continue
            stdscr.addstr(i, 0, f"{k}", curses.color_pair(2))
            i += 1
            if isinstance(current_record[k], dict):
                i += 1
                for y in current_record[k].keys():
                    stdscr.addstr(i, len(k) + 1, f"{y}", curses.color_pair(1))
                    stdscr.addstr(i, len(k) + len(y) + 2, f"{current_record[k][y]}", curses.color_pair(2))
                    i += 1
            else:
                stdscr.addstr(i, len(k) + 1, f"{current_record[k]}", curses.color_pair(1))
            i += 1
        stdscr.addstr(i, 0, f"{current_record['doc']}", curses.color_pair(2))
#        stdscr.addstr(2, 0, f"{current_record['id']}\n{current_record}")
        # recs = []
        # for k in current_record.keys():
        #     recs.append((f"{k}\t{current_record[k]}"))
        # recstr = "\n".join(recs)
        # stdscr.addstr(2, 0, f"{current_record['id']}\n{recstr}")




        # --=={ MAIN }==--

        # Get user input
        key = stdscr.getch()

        # Handle user input
        if key == curses.KEY_LEFT:
            current_collection_index = (current_collection_index - 1) % len(collections)
        elif key == curses.KEY_RIGHT:
            current_collection_index = (current_collection_index + 1) % len(collections)
        elif key == curses.KEY_UP:
            current_record_index = (current_record_index - 1) % len(current_records)
        elif key == curses.KEY_DOWN:
            current_record_index = (current_record_index + 1) % len(current_records)
        elif key == ord('q'):
            break

if __name__ == "__main__":
    curses.wrapper(main)
