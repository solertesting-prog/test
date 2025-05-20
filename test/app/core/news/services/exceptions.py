from uuid import UUID


class NewsArticleNotFound(Exception):
    """Exception raised when a news article is not found."""

    def __init__(self, article_id: UUID | None):
        self.article_id = article_id
        super().__init__(f"News article with ID {article_id} not found.")
