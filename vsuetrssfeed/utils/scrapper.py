from asyncio import create_task, gather
from typing import Collection

from aiohttp import ClientSession as HttpClient
from bs4 import BeautifulSoup, PageElement, ResultSet
from vsuetrssfeed.models import News


class VsuetScrapper(object):
    """
    Скраппер новостей с ресурса VSUET
    """

    vsuet_base_url: str
    news_endpoint: str

    def __init__(self, vsuet_base_url: str, news_endpoint: str) -> None:
        """
        Скраппер новостей с ресурса VSUET

        :param vsuet_base_url: Основной домен ресурса vsuet
        :param news_endpoint: Подстраница с новостями
        """
        self.vsuet_base_url = vsuet_base_url
        self.news_endpoint = news_endpoint

    async def _get_request(self, endpoint: str = "") -> str:
        """
        Выполняет GET запрос к ресурсу

        :param endpoint: Конечная цель запроса
        :return: Текст ответа запроса
        """
        async with HttpClient() as session:
            request = await session.get(
                f"{self.vsuet_base_url}{self.news_endpoint}{endpoint}"
            )
            if request.status == 200:
                return await request.text(encoding="utf-8")
            raise ConnectionError(
                f"Ошибка подключения к сайту {self.vsuet_base_url}: {request.status}"
            )

    async def _get_news_divs(self, page: int | None = None) -> ResultSet[PageElement]:
        """
        Получает html-представления новостей с ресурса vsuet

        :param page: номер страницы, с которой будут получены новости
        :return: Объединение элементов страницы с новостями
        """
        endpoint = ""
        if page is not None:
            endpoint = f"?start={page * 15}"
        page = BeautifulSoup(await self._get_request(endpoint), "html.parser")
        feed = page.find("div", class_="news news-box-category").find(
            "div", class_="row no-indents"
        )
        return feed.find_all("div", class_="news__item")

    def _get_news_model(self, news: PageElement) -> News:
        """
        Преобразует html-представление новсти в модель
        :param news: bs4-элемент с новостью
        :return: Модель новости
        """
        title = news.find("h3", class_="news__title")
        href = title.find("a").get("href")
        tags = news.find_all("a", class_="btn-sm label label-info")
        description = news.find("div", class_="news__intro").text.strip()
        image = f"{self.vsuet_base_url}{news.find("div", class_="preview-img")["style"].split()[1][4:-2]}"
        return News(
            title=title.text.strip(),
            link=f"{self.vsuet_base_url}{href}",
            description=f'<img src="{image}" /><p>{description}',
            pubdate=news.find("div", class_="news__datetime").text.strip(),
            guid=href.split("/")[-1],
            categories=list(map(lambda tag: tag.text.strip(), tags)),
        )

    async def _form_feed(self, page: int) -> Collection[News]:
        """
        Формирует список с моделями новостей по заданной странице
        :param page: Номер страницы
        :return: список новостей
        """
        return list(
            map(
                lambda news: self._get_news_model(news), await self._get_news_divs(page)
            )
        )

    async def get_feed(self, pages: int | None = None) -> Collection[News]:
        """
        Формирует список новостей по заданному кол-ву страниц
        :param pages: Кол-во страниц
        :return: Список новостей
        """
        if pages is None:
            return await self._form_feed(0)
        tasks = tuple(map(lambda i: create_task(self._form_feed(i)), range(0, pages)))
        results = await gather(*tasks)
        feed = []
        for result in results:
            feed.extend(result)
        return feed
