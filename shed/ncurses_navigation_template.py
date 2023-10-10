import curses

# Mocked Chroma database data
collections = ["Collection1", "Collection2", "Collection3"]
records = {
    "Collection1": ["Record1", "Record2", "Record3"],
    "Collection2": ["RecordA", "RecordB", "RecordC"],
    "Collection3": ["DataX", "DataY", "DataZ"],
}

def main(stdscr):
    curses.curs_set(0)  # Hide the cursor
    current_collection_index = 0
    current_record_index = 0

    while True:
        stdscr.clear()

        # Get the current collection and its records
        current_collection = collections[current_collection_index]
        current_records = records[current_collection]

        # Display the current collection name at the top
        stdscr.addstr(0, 0, f"Current Collection: {current_collection}")

        # Display the current record
        current_record = current_records[current_record_index]
        stdscr.addstr(2, 0, f"Current Record: {current_record}")

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
