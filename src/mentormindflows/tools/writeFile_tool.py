import os
from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class WriteFileToolInput(BaseModel):
    filename: str = Field(..., description="Name of the file to write to.")
    content: str = Field(..., description="Content to write into the file.")
    directory: str = Field(default="outputs", description="Directory where the file will be created.")
    overwrite: bool = Field(default=True, description="Whether to overwrite the file if it already exists.")


class WriteFileTool(BaseTool):
    name: str = "Write File Tool"
    description: str = (
        "A tool to write content to a specified file. "
        "Accepts filename, content, and optionally a directory path and overwrite flag as input."
    )
    args_schema: Type[BaseModel] = WriteFileToolInput

    def _run(self, filename: str, content: str, directory: str = "outputs", overwrite: bool = True) -> str:
        # Ensure the directory exists
        os.makedirs(directory, exist_ok=True)

        # Construct the full file path
        file_path = os.path.join(directory, filename)

        # Check if the file exists and handle overwrite logic
        if os.path.exists(file_path) and not overwrite:
            return f"⚠️ File '{file_path}' already exists and overwrite is set to False."

        # Write the content to the file
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            return f"✅ Content successfully written to '{file_path}'."
        except Exception as e:
            return f"❌ Failed to write to file '{file_path}': {e}"

    def _arun(self, *args, **kwargs):
        raise NotImplementedError("Async execution is not supported for WriteFileTool.")