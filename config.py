"""
This module is responsible for accessing sensitive information stored in the
`.env` file and extracting the Alpha Vantage API key so it can be used
securely throughout different parts of the project.
"""
import os
from pydantic_settings import BaseSettings


def return_full_path(filename: str = ".env") -> str:
    absolute_path = os.path.abspath(__file__)
    directory_name = os.path.dirname(absolute_path)
    return os.path.join(directory_name, filename)   


class Settings(BaseSettings):
    """Use pydantic to define settings for this project"""
    alpha_vantage_api_key :str
    db_name: str = ""
    model_directory: str = ""
    
    class Config:
        """internal class to handle settings loading, in out project fort the 'path' """
        env_file = return_full_path(".env")
settings = Settings()
        

        
    
    
    