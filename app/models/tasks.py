from __future__ import annotations

from typing import List

from pydantic import BaseModel


class NamesOfFailedFileItem(BaseModel):
    input_file_name: str
    error_message: str


class NamesOfSuccessFileItem(BaseModel):
    input_file_name: str
    output_file_name: str


class Completed(BaseModel):
    number_of_files: int
    names_of_file: List[NamesOfSuccessFileItem]


class Error(BaseModel):
    number_of_files: int
    names_of_file: List[NamesOfFailedFileItem]


class Task(BaseModel):
    task_id: str
    number_of_files: int
    completed: Completed
    error: Error


"""
Mentioed is the format of json
{
    "task_id": "str",
    "number_of_files": 2,
    "completed": {
        "number_of_files": 2,
        "names_of_file":[
            {
                "input_file_name": "input name",
                "output_file_name": "output name"
            },
            {
                "input_file_name": "input name",
                "output_file_name": "output name"
            }
        ]
    },
    "error": {
        "number_of_files" : 2,
        "names_of_file": [
            "file1",
            "file2"
            ]
    }
}
"""
