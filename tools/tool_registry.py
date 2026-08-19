from tools.browser_tool import BrowserTool
from tools.calendar_tool import CalendarTool
from tools.file_manager import FileManagerTool
from tools.gmail_tool import GmailTool
from tools.web_search import WebSearchTool


class ToolRegistry:
    def __init__(self) -> None:
        self._tools = {
            "web_search": WebSearchTool(),
            "file_manager": FileManagerTool(),
            "gmail": GmailTool(),
            "calendar": CalendarTool(),
            "browser": BrowserTool(),
        }

    def get_tool(self, name: str):
        return self._tools[name]

    def list_tools(self) -> list[str]:
        return sorted(self._tools.keys())
