import couchdb
import sys
import json

class CouchDBLoader:
    def __init__(self, server_url):
        self.server = couchdb.Server(server_url)
        self.data = []

    def read_from_stdin(self):
        """Read JSON data from stdin and store it in the class."""
        for line in sys.stdin:
            try:
                item = json.loads(line.strip())
                self.data.append(item)
            except json.JSONDecodeError:
                print(f"Invalid JSON: {line.strip()}")

    def load_from_list(self, data_list):
        """Load data from a list of dictionaries."""
        self.data.extend(data_list)

    def load_into_database(self, db_name):
        """Load the stored data into a named CouchDB database."""
        if db_name not in self.server:
            db = self.server.create(db_name)
        else:
            db = self.server[db_name]

        for item in self.data:
            db.save(item)

        print(f"Loaded {len(self.data)} documents into '{db_name}' database.")

    def load_from_database(self, db_name, filter_function=None):
        """
        Load data from a named CouchDB database and store it in the class.
        
        :param db_name: Name of the database to load from
        :param filter_function: Optional function to filter documents
        """
        if db_name not in self.server:
            print(f"Database '{db_name}' does not exist.")
            return

        db = self.server[db_name]
        
        if filter_function:
            self.data = [doc for doc in db.view('_all_docs', include_docs=True) if filter_function(doc['doc'])]
        else:
            self.data = [doc['doc'] for doc in db.view('_all_docs', include_docs=True)]
        
        print(f"Loaded {len(self.data)} documents from '{db_name}' database.")

    def process_data(self, functions):
        """Apply a list of functions to the stored data."""
        for func in functions:
            self.data = [func(item) for item in self.data]

    def clear_data(self):
        """Clear the stored data."""
        self.data = []

    def get_data(self):
        """Return the stored data."""
        return self.data

# ---->
# Initialize the loader
loader = CouchDBLoader("http://admin:password@localhost:5984")

# Define a filter function
def filter_by_type(doc):
    return doc.get('type') == 'user'

# Load data from a database, only including documents where type is 'user'
loader.load_from_database('my_database', filter_function=filter_by_type)

# Now loader.data contains only the documents that passed the filter
