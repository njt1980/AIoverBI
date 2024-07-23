from typing import Optional, Type
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool

class SendEmailInput(BaseModel):
    emailid:str = Field(description = "Email id to which email has to be send")
    emailtext:str = Field(description = "Text to be included in the email")


class SendEmailTool(BaseTool):
    name = "send_email";
    description = "Send email and provide confirmation that the email has been successfully sent or not";
    args_schema:Type[BaseModel] = SendEmailInput

    def _run(self,emailid:str,emailtext:str) -> str:
        result = "Successfully";
        return f"Email {result} to {emailid}"