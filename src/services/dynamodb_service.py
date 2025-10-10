"""DynamoDB service for database operations."""
import logging
from typing import Optional, Dict, Any, List
import boto3
from botocore.exceptions import ClientError
from src.config import get_settings

logger = logging.getLogger(__name__)


class DynamoDBService:
    """Service for DynamoDB operations."""

    def __init__(self):
        """Initialize DynamoDB service."""
        self.settings = get_settings()
        self.dynamodb = boto3.resource(
            "dynamodb",
            region_name=self.settings.aws_region,
            aws_access_key_id=self.settings.aws_access_key_id,
            aws_secret_access_key=self.settings.aws_secret_access_key,
        )
        self.client = boto3.client(
            "dynamodb",
            region_name=self.settings.aws_region,
            aws_access_key_id=self.settings.aws_access_key_id,
            aws_secret_access_key=self.settings.aws_secret_access_key,
        )

    def create_tables(self):
        """Create all required DynamoDB tables if they don't exist."""
        tables = [
            {
                "TableName": self.settings.dynamodb_patients_table,
                "KeySchema": [{"AttributeName": "patient_id", "KeyType": "HASH"}],
                "AttributeDefinitions": [{"AttributeName": "patient_id", "AttributeType": "S"}],
                "BillingMode": "PAY_PER_REQUEST",
            },
            {
                "TableName": self.settings.dynamodb_consultations_table,
                "KeySchema": [{"AttributeName": "consultation_id", "KeyType": "HASH"}],
                "AttributeDefinitions": [
                    {"AttributeName": "consultation_id", "AttributeType": "S"},
                    {"AttributeName": "patient_id", "AttributeType": "S"},
                ],
                "GlobalSecondaryIndexes": [
                    {
                        "IndexName": "patient_id-index",
                        "KeySchema": [{"AttributeName": "patient_id", "KeyType": "HASH"}],
                        "Projection": {"ProjectionType": "ALL"},
                    }
                ],
                "BillingMode": "PAY_PER_REQUEST",
            },
            {
                "TableName": self.settings.dynamodb_triage_table,
                "KeySchema": [{"AttributeName": "triage_id", "KeyType": "HASH"}],
                "AttributeDefinitions": [
                    {"AttributeName": "triage_id", "AttributeType": "S"},
                    {"AttributeName": "patient_id", "AttributeType": "S"},
                ],
                "GlobalSecondaryIndexes": [
                    {
                        "IndexName": "patient_id-index",
                        "KeySchema": [{"AttributeName": "patient_id", "KeyType": "HASH"}],
                        "Projection": {"ProjectionType": "ALL"},
                    }
                ],
                "BillingMode": "PAY_PER_REQUEST",
            },
        ]

        for table_config in tables:
            try:
                self.client.describe_table(TableName=table_config["TableName"])
                logger.info(f"Table {table_config['TableName']} already exists")
            except ClientError as e:
                if e.response["Error"]["Code"] == "ResourceNotFoundException":
                    try:
                        self.client.create_table(**table_config)
                        logger.info(f"Created table {table_config['TableName']}")
                    except ClientError as create_error:
                        logger.error(f"Error creating table: {create_error}")
                else:
                    logger.error(f"Error checking table: {e}")

    def put_item(self, table_name: str, item: Dict[str, Any]) -> bool:
        """Put an item into a DynamoDB table."""
        try:
            table = self.dynamodb.Table(table_name)
            table.put_item(Item=item)
            logger.info(f"Successfully put item in {table_name}")
            return True
        except ClientError as e:
            logger.error(f"Error putting item in {table_name}: {e}")
            return False

    def get_item(self, table_name: str, key: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Get an item from a DynamoDB table."""
        try:
            table = self.dynamodb.Table(table_name)
            response = table.get_item(Key=key)
            return response.get("Item")
        except ClientError as e:
            logger.error(f"Error getting item from {table_name}: {e}")
            return None

    def query_by_index(
        self, table_name: str, index_name: str, key_name: str, key_value: str
    ) -> List[Dict[str, Any]]:
        """Query items by secondary index."""
        try:
            table = self.dynamodb.Table(table_name)
            response = table.query(
                IndexName=index_name,
                KeyConditionExpression=f"{key_name} = :value",
                ExpressionAttributeValues={":value": key_value},
            )
            return response.get("Items", [])
        except ClientError as e:
            logger.error(f"Error querying {table_name} by index: {e}")
            return []

    def update_item(
        self, table_name: str, key: Dict[str, Any], updates: Dict[str, Any]
    ) -> bool:
        """Update an item in a DynamoDB table."""
        try:
            table = self.dynamodb.Table(table_name)
            update_expression = "SET " + ", ".join([f"{k} = :{k}" for k in updates.keys()])
            expression_values = {f":{k}": v for k, v in updates.items()}

            table.update_item(
                Key=key,
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_values,
            )
            logger.info(f"Successfully updated item in {table_name}")
            return True
        except ClientError as e:
            logger.error(f"Error updating item in {table_name}: {e}")
            return False

    def scan_table(self, table_name: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Scan a table and return all items."""
        try:
            table = self.dynamodb.Table(table_name)
            if limit:
                response = table.scan(Limit=limit)
            else:
                response = table.scan()
            return response.get("Items", [])
        except ClientError as e:
            logger.error(f"Error scanning {table_name}: {e}")
            return []
