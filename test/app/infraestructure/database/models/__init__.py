from .news import NewsArticle as NewsArticleModel
from .users import User as UserModel


__beanie_models__ = [NewsArticleModel, UserModel]