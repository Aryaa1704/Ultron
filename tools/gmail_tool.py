class GmailTool:
    async def send_email(self, to_email: str, subject: str, body: str) -> str:
        return f"Prepared Gmail send task to {to_email} with subject '{subject}'."
