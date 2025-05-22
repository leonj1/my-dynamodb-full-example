#!/usr/bin/env python3
"""
DynamoDB CRUD Operations Script

This script demonstrates Create, Read, Update, and Delete operations
on a local DynamoDB table running in LocalStack.
"""

import boto3
import uuid
import time
import json
from datetime import datetime
from botocore.exceptions import ClientError

# Configure boto3 client to use LocalStack
def get_dynamodb_client():
    """Create and return a DynamoDB client configured for LocalStack."""
    return boto3.client(
        'dynamodb',
        endpoint_url='http://localhost:4566',  # LocalStack endpoint
        region_name='us-east-1',
        aws_access_key_id='test',
        aws_secret_access_key='test'
    )

def get_dynamodb_resource():
    """Create and return a DynamoDB resource configured for LocalStack."""
    return boto3.resource(
        'dynamodb',
        endpoint_url='http://localhost:4566',  # LocalStack endpoint
        region_name='us-east-1',
        aws_access_key_id='test',
        aws_secret_access_key='test'
    )

# Table name as defined in Terraform
TABLE_NAME = 'example-table'

# CRUD Operations
def create_item(name, email, additional_data=None):
    """
    Create a new item in the DynamoDB table.
    
    Args:
        name (str): Name of the person/item
        email (str): Email address (used for GSI)
        additional_data (dict, optional): Any additional data to store
    
    Returns:
        dict: The created item
    """
    client = get_dynamodb_client()
    
    # Generate a unique ID
    item_id = str(uuid.uuid4())
    timestamp = int(time.time())
    
    # Prepare the item
    item = {
        'id': {'S': item_id},
        'name': {'S': name},
        'email': {'S': email},
        'created_at': {'N': str(timestamp)},
        'updated_at': {'N': str(timestamp)}
    }
    
    # Add any additional data
    if additional_data:
        for key, value in additional_data.items():
            # Determine the DynamoDB type
            if isinstance(value, str):
                item[key] = {'S': value}
            elif isinstance(value, (int, float)):
                item[key] = {'N': str(value)}
            elif isinstance(value, bool):
                item[key] = {'BOOL': value}
            elif isinstance(value, (list, dict)):
                item[key] = {'S': json.dumps(value)}
    
    # Put the item in the table
    client.put_item(
        TableName=TABLE_NAME,
        Item=item
    )
    
    print(f"Created item with ID: {item_id}")
    return item

def read_item(item_id):
    """
    Read an item from the DynamoDB table by its ID.
    
    Args:
        item_id (str): The ID of the item to read
    
    Returns:
        dict: The item if found, None otherwise
    """
    client = get_dynamodb_client()
    
    try:
        response = client.get_item(
            TableName=TABLE_NAME,
            Key={'id': {'S': item_id}}
        )
        
        if 'Item' in response:
            print(f"Found item: {response['Item']}")
            return response['Item']
        else:
            print(f"No item found with ID: {item_id}")
            return None
    
    except ClientError as e:
        print(f"Error reading item: {e}")
        return None

def update_item(item_id, update_data):
    """
    Update an existing item in the DynamoDB table.
    
    Args:
        item_id (str): The ID of the item to update
        update_data (dict): Dictionary of attributes to update
    
    Returns:
        bool: True if update was successful, False otherwise
    """
    client = get_dynamodb_client()
    
    # Prepare update expression and attribute values
    update_expressions = []
    expression_attribute_values = {}
    expression_attribute_names = {}
    
    # Add updated_at timestamp
    update_expressions.append("#updated_at = :updated_at")
    expression_attribute_values[":updated_at"] = {"N": str(int(time.time()))}
    expression_attribute_names["#updated_at"] = "updated_at"
    
    # Add other updates
    for i, (key, value) in enumerate(update_data.items()):
        placeholder = f":val{i}"
        name_placeholder = f"#attr{i}"
        
        update_expressions.append(f"{name_placeholder} = {placeholder}")
        expression_attribute_names[name_placeholder] = key
        
        # Determine the DynamoDB type
        if isinstance(value, str):
            expression_attribute_values[placeholder] = {"S": value}
        elif isinstance(value, (int, float)):
            expression_attribute_values[placeholder] = {"N": str(value)}
        elif isinstance(value, bool):
            expression_attribute_values[placeholder] = {"BOOL": value}
        elif isinstance(value, (list, dict)):
            expression_attribute_values[placeholder] = {"S": json.dumps(value)}
    
    update_expression = "SET " + ", ".join(update_expressions)
    
    try:
        response = client.update_item(
            TableName=TABLE_NAME,
            Key={'id': {'S': item_id}},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ExpressionAttributeNames=expression_attribute_names,
            ReturnValues="UPDATED_NEW"
        )
        
        print(f"Updated item with ID: {item_id}")
        print(f"Updated attributes: {response.get('Attributes', {})}")
        return True
    
    except ClientError as e:
        print(f"Error updating item: {e}")
        return False

def delete_item(item_id):
    """
    Delete an item from the DynamoDB table.
    
    Args:
        item_id (str): The ID of the item to delete
    
    Returns:
        bool: True if deletion was successful, False otherwise
    """
    client = get_dynamodb_client()
    
    try:
        client.delete_item(
            TableName=TABLE_NAME,
            Key={'id': {'S': item_id}}
        )
        
        print(f"Deleted item with ID: {item_id}")
        return True
    
    except ClientError as e:
        print(f"Error deleting item: {e}")
        return False

def query_by_email(email):
    """
    Query items by email using the Global Secondary Index.
    
    Args:
        email (str): Email to search for
    
    Returns:
        list: List of items matching the email
    """
    client = get_dynamodb_client()
    
    try:
        response = client.query(
            TableName=TABLE_NAME,
            IndexName='email-index',
            KeyConditionExpression='email = :email',
            ExpressionAttributeValues={
                ':email': {'S': email}
            }
        )
        
        items = response.get('Items', [])
        print(f"Found {len(items)} items with email: {email}")
        return items
    
    except ClientError as e:
        print(f"Error querying by email: {e}")
        return []

def query_by_created_at(timestamp, comparison_operator='='):
    """
    Query items by created_at timestamp using the Global Secondary Index.
    
    Args:
        timestamp (int): Unix timestamp to search for
        comparison_operator (str): One of '=', '<', '<=', '>', '>='
    
    Returns:
        list: List of items matching the criteria
    """
    client = get_dynamodb_client()
    
    operator_map = {
        '=': '=',
        '<': '<',
        '<=': '<=',
        '>': '>',
        '>=': '>='
    }
    
    if comparison_operator not in operator_map:
        print(f"Invalid comparison operator: {comparison_operator}")
        return []
    
    try:
        response = client.query(
            TableName=TABLE_NAME,
            IndexName='created-at-index',
            KeyConditionExpression=f'created_at {operator_map[comparison_operator]} :timestamp',
            ExpressionAttributeValues={
                ':timestamp': {'N': str(timestamp)}
            }
        )
        
        items = response.get('Items', [])
        print(f"Found {len(items)} items with created_at {comparison_operator} {timestamp}")
        return items
    
    except ClientError as e:
        print(f"Error querying by created_at: {e}")
        return []

def scan_table(filter_expression=None, expression_attribute_values=None):
    """
    Scan the entire table, optionally with a filter.
    
    Args:
        filter_expression (str, optional): Filter expression
        expression_attribute_values (dict, optional): Values for the filter expression
    
    Returns:
        list: All items in the table matching the filter
    """
    client = get_dynamodb_client()
    
    scan_kwargs = {
        'TableName': TABLE_NAME
    }
    
    if filter_expression and expression_attribute_values:
        scan_kwargs['FilterExpression'] = filter_expression
        scan_kwargs['ExpressionAttributeValues'] = expression_attribute_values
    
    try:
        response = client.scan(**scan_kwargs)
        items = response.get('Items', [])
        
        # Handle pagination if there are more items
        while 'LastEvaluatedKey' in response:
            scan_kwargs['ExclusiveStartKey'] = response['LastEvaluatedKey']
            response = client.scan(**scan_kwargs)
            items.extend(response.get('Items', []))
        
        print(f"Found {len(items)} items in table")
        return items
    
    except ClientError as e:
        print(f"Error scanning table: {e}")
        return []

def list_tables():
    """List all DynamoDB tables in the LocalStack instance."""
    client = get_dynamodb_client()
    
    try:
        response = client.list_tables()
        tables = response.get('TableNames', [])
        print(f"Available tables: {tables}")
        return tables
    
    except ClientError as e:
        print(f"Error listing tables: {e}")
        return []

def describe_table(table_name=TABLE_NAME):
    """
    Describe the specified DynamoDB table.
    
    Args:
        table_name (str): Name of the table to describe
    
    Returns:
        dict: Table description
    """
    client = get_dynamodb_client()
    
    try:
        response = client.describe_table(TableName=table_name)
        table_description = response.get('Table', {})
        print(f"Table description: {json.dumps(table_description, indent=2, default=str)}")
        return table_description
    
    except ClientError as e:
        print(f"Error describing table: {e}")
        return {}

def print_item_readable(item):
    """
    Convert a DynamoDB item to a more readable format.
    
    Args:
        item (dict): DynamoDB item with attribute types
    
    Returns:
        dict: Item with simplified attribute values
    """
    if not item:
        return None
    
    readable = {}
    for key, value in item.items():
        # Extract the actual value based on its type
        if 'S' in value:
            readable[key] = value['S']
        elif 'N' in value:
            readable[key] = float(value['N']) if '.' in value['N'] else int(value['N'])
        elif 'BOOL' in value:
            readable[key] = value['BOOL']
        elif 'L' in value:
            readable[key] = [print_item_readable(i) if isinstance(i, dict) else i for i in value['L']]
        elif 'M' in value:
            readable[key] = print_item_readable(value['M'])
        else:
            readable[key] = value
    
    return readable

def demo():
    """Run a demonstration of all CRUD operations."""
    print("\n=== DynamoDB CRUD Demo ===\n")
    
    # Check if our table exists
    tables = list_tables()
    if TABLE_NAME not in tables:
        print(f"Table '{TABLE_NAME}' not found. Make sure to run 'make all-up' first.")
        return
    
    # Describe the table
    describe_table()
    
    # Create items
    print("\n--- Creating Items ---")
    item1 = create_item("John Doe", "john@example.com", {"age": 30, "city": "New York"})
    item2 = create_item("Jane Smith", "jane@example.com", {"age": 25, "city": "San Francisco"})
    
    # Convert to readable format
    item1_id = item1['id']['S']
    item2_id = item2['id']['S']
    
    # Read items
    print("\n--- Reading Items ---")
    retrieved_item1 = read_item(item1_id)
    print("Retrieved item 1 (readable):", json.dumps(print_item_readable(retrieved_item1), indent=2))
    
    # Update an item
    print("\n--- Updating Items ---")
    update_item(item1_id, {"age": 31, "status": "active"})
    
    # Read the updated item
    updated_item1 = read_item(item1_id)
    print("Updated item 1 (readable):", json.dumps(print_item_readable(updated_item1), indent=2))
    
    # Query by email
    print("\n--- Querying by Email ---")
    email_results = query_by_email("jane@example.com")
    for item in email_results:
        print("Item found by email (readable):", json.dumps(print_item_readable(item), indent=2))
    
    # Scan the table
    print("\n--- Scanning Table ---")
    all_items = scan_table()
    print(f"Found {len(all_items)} items in total")
    
    # Delete an item
    print("\n--- Deleting Items ---")
    delete_item(item2_id)
    
    # Verify deletion
    remaining_items = scan_table()
    print(f"Remaining items after deletion: {len(remaining_items)}")
    
    print("\n=== Demo Complete ===")

if __name__ == "__main__":
    demo()
