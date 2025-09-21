from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from .gmail_utility import authenticate_gmail, create_message, create_draft, send_email

class GmailToolInput(BaseModel):
    """Input schema for GmailTool."""
    touser: str = Field(..., description="The recipient's email address.")
    body: str = Field(..., description="The body of the email to send.")

class GmailTool(BaseTool):
    name: str = "GmailTool"
    description: str = (
        "A tool to create Gmail drafts. Provide the recipient's email address and the body of the email."
    )
    args_schema: Type[BaseModel] = GmailToolInput

    def _run(self, touser: str, body: str) -> str:
        try:
            service = authenticate_gmail()

            sender = "d2021.manrajsingh.virdi@ves.ac.in"
            subject = "First Responder Report"
            message_text = body
            print(f"Message text: {message_text}")
            message = create_message(sender, touser, subject, message_text)
            draft = create_draft(service, "me", message)

            print(f"Email draft created successfully! Draft id: {draft['id']}")
            sent = send_email(service, "me", message)
            if sent:
                return f"Email sent successfully! Message ID: {sent['id']}"
            else:
                return "Failed to send the email."

        except Exception as e:
            return f"Error creating email draft: {e}"