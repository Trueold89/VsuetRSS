from xml.etree.ElementTree import Element, SubElement, tostring

from vsuetrssfeed.models import Feed, News


class XMLGenerator(object):
    """
    Генератор XML документов из моделей
    """

    @staticmethod
    def _add_tag(news: Element, tag: str) -> None:
        """
        Добавляет категорию новости
        :param news: Элемент новости
        :param tag: Категория
        """
        category = SubElement(news, "category")
        category.text = tag

    def translate_news(self, parent: Element, news: News) -> None:
        """
        Переводит новость в XML
        :param parent: Родительский объект
        :param news: Новость
        """
        item = SubElement(parent, "item")
        title = SubElement(item, "title")
        link = SubElement(item, "link")
        description = SubElement(item, "description")
        pubdate = SubElement(item, "pubDate")
        guid = SubElement(item, "guid")
        title.text = news.title
        link.text = news.link
        description.text = news.description
        pubdate.text = news.pubdate
        guid.text = news.guid
        for tag in news.categories:
            self._add_tag(item, tag)

    def translate_feed(self, feed: Feed) -> str:
        """
        Переводит ленту новостей в XML
        :param feed: Лента новостей
        """
        root = Element("rss", version=feed.rss_version)
        channel = SubElement(root, "channel")
        title = SubElement(channel, "title")
        link = SubElement(channel, "link")
        description = SubElement(channel, "description")
        language = SubElement(channel, "language")
        pubdate = SubElement(channel, "pubDate")
        title.text = feed.title
        link.text = feed.link
        description.text = feed.description
        language.text = feed.language
        pubdate.text = feed.pubDate
        for news in feed.items:
            self.translate_news(channel, news)
        return tostring(root, encoding="utf-8", method="xml")


def gen_xml(feed: Feed) -> str:
    """
    Генерирует XML запись ленты новостей
    :param feed: Лента новостей
    :return:
    """
    return XMLGenerator().translate_feed(feed)
