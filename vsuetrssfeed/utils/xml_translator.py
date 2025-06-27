from xml.etree.ElementTree import Element, SubElement, ElementTree, tostring

from vsuetrssfeed.models import Feed, News


class XMLGenerator(object):

    @staticmethod
    def _add_tag(news: Element, tag: str) -> None:
        category = SubElement(news, "category")
        category.text = tag

    def translate_news(self, parent: Element, news: News) -> None:
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
        root = Element('rss', version=feed.rss_version)
        channel = SubElement(root, 'channel')
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
