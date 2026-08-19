from dataclasses import dataclass


@dataclass
class SearchResult:
    title: str
    url: str
    snippet: str


class WebSearchTool:
    async def search(self, query: str) -> list[SearchResult]:
        return [
            SearchResult(
                title="Search integration placeholder",
                url="https://example.com",
                snippet=f"Wire your search provider for query: {query}",
            )
        ]
