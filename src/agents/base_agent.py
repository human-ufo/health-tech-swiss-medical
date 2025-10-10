"""Base agent class with AWS Bedrock integration."""
import logging
from typing import Optional
import boto3
from langchain_aws import ChatBedrock
from src.config import get_settings

logger = logging.getLogger(__name__)


class BaseAgent:
    """Base class for all agents."""

    def __init__(self, model_id: Optional[str] = None, temperature: float = 0.7):
        """Initialize base agent with Bedrock LLM."""
        self.settings = get_settings()
        self.model_id = model_id or self.settings.bedrock_model_id

        # Initialize Bedrock client
        self.bedrock_client = boto3.client(
            service_name="bedrock-runtime",
            region_name=self.settings.bedrock_region,
            aws_access_key_id=self.settings.aws_access_key_id,
            aws_secret_access_key=self.settings.aws_secret_access_key,
        )

        # Initialize LangChain Bedrock LLM
        self.llm = ChatBedrock(
            client=self.bedrock_client,
            model_id=self.model_id,
            model_kwargs={
                "temperature": temperature,
                "top_p": 0.9,
                "max_tokens": 2048,
            },
        )

        logger.info(f"Initialized {self.__class__.__name__} with model {self.model_id}")

    def invoke(self, prompt: str) -> str:
        """Invoke the LLM with a prompt."""
        try:
            response = self.llm.invoke(prompt)
            return response.content
        except Exception as e:
            logger.error(f"Error invoking LLM: {e}")
            raise
