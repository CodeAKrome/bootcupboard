import curses
import chromadb
import sys

# Do you Mock me, Sir?
# Faux Chroma database data
# collections = ["Collection1", "Collection2", "Collection3"]
# records = {}
# for c in collections:
#     records[c] = []
#     tids = [c+"ID1", c+"ID2", c+"ID3"]
#     tdocs = [c+"Doc1", c+"Doc2", c+"Doc3"]
#     tmeta = [c+"Metadata1", c+"Metadata2", c+"Metadata3"]
#     for i, d, m in zip(tids, tdocs, tmeta):
#         records[c].append({"id":i,"doc":d,"meta":m})


records = {}
try: 
    client = chromadb.PersistentClient(path=sys.argv[1])
except Exception as e:
    print("Error:", e)
    sys.exit(1)
    
colls = client.list_collections()
print("Num Collections: ", len(colls))
collections = [c.name for c in colls]
for collection in collections:
    print("Collection: ", collection)
    cc_handle = client.get_collection(collection)
    data = cc_handle.get()
    n = len(data)
    if n > 0:
        print("Num Records: ", n)
        records[collection] = []
        ids = data["ids"]
        docs = data["documents"]
        meta = data["metadatas"]
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
        n = len(current_records)
        # Display the current collection name at the top of the page, highlighted in bold.
        stdscr.addstr(0, 0, f"{current_collection} {current_record_index} / {n}", curses.color_pair(1))
        # --=={ Display the current record }==--
        current_record = current_records[current_record_index]
        stdscr.addstr(2, 0, f"{current_record['id']}")
        # indentation
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
