from rich.table import Table


def print_table(data: dict):
    table = Table()

    # Add the column headers.
    for key in data.keys():
        table.add_column(key)

    # Add the rows of data.
    for row in data.values():
        table.add_row(*row)


# Print the table.
#print(table)
data = {
    "Name": ["Alice", "Bob", "Carol"],
    "Age": [25, 30, 35],
    "City": ["London", "Paris", "New York"],
}

print_table(data)
