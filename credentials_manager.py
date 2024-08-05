"""
Module: Credentials Manager

This module defines a CredentialsManager class that abstracts the management and retrieval of credentials
for various APIs and services used throughout the application.
"""
import os
from dotenv import load_dotenv


class CredentialsManager:
    """
    A class to manage and retrieve credentials safely from environment variables.

    This class abstracts away the source of the environmental variables, providing
    a single point of retrieval for credentials used throughout the application.
    """

    def __init__(self):
        """
        Initializes the CredentialsManager and loads the environment variables.
        """
        load_dotenv()  # Load environment variables from a .env file, if present

    def get_credential(self, key: str) -> str:
        """
        Retrieves a credential using its key.

        Args:
            key (str): The key corresponding to the credential.
        """
        value = os.getenv(key)
        if value is None:
            raise ValueError(f"Credential for '{key}' not found.")
        return value
