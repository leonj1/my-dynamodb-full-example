# DynamoDB CRUD Operations with Python

This Python script demonstrates how to perform CRUD (Create, Read, Update, Delete) operations on a DynamoDB table running locally in LocalStack.

## Prerequisites

- LocalStack and Terraform infrastructure must be running (use `make all-up` to start everything)
- Python 3.6 or higher
- Required Python packages (install with `pip install -r requirements.txt`)

## Features

The script provides the following functionality:

- **Create**: Add new items to the DynamoDB table
- **Read**: Retrieve items by their ID
- **Update**: Modify existing items
- **Delete**: Remove items from the table
- **Query**: Search for items using the Global Secondary Indexes (email, created_at)
- **Scan**: Retrieve all items from the table, optionally with filters
- **Utility Functions**: List tables, describe table structure, format items for readability

## Usage

1. Start the LocalStack container and apply Terraform configuration:
   ```
   make all-up
   ```

2. Install required Python packages:
   ```
   pip install -r requirements.txt
   ```

3. Run the demo script:
   ```
   python dynamodb_crud.py
   ```

## Customizing

The script is designed to work with the `example-table` defined in the Terraform configuration. The table has the following structure:

- Primary key: `id` (String)
- Global Secondary Indexes:
  - `email-index`: Hash key on `email` (String)
  - `created-at-index`: Hash key on `created_at` (Number)

You can modify the script to work with different tables or add additional functionality as needed.

## Functions

- `create_item(name, email, additional_data=None)`: Create a new item
- `read_item(item_id)`: Read an item by ID
- `update_item(item_id, update_data)`: Update an existing item
- `delete_item(item_id)`: Delete an item
- `query_by_email(email)`: Query items by email
- `query_by_created_at(timestamp, comparison_operator='=')`: Query items by creation timestamp
- `scan_table(filter_expression=None, expression_attribute_values=None)`: Scan the entire table
- `list_tables()`: List all DynamoDB tables
- `describe_table(table_name=TABLE_NAME)`: Describe table structure
- `print_item_readable(item)`: Convert DynamoDB item to readable format
