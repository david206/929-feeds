#!/usr/bin/env python
# coding: utf-8

import PyRSS2Gen
import feedparser
import datetime
import copy

url_feed_929 = 'http://feeds.soundcloud.com/users/soundcloud:users:166708775/sounds.rss'

def filter_feed(feed, keywords, exclusive=False):
    if isinstance(keywords, basestring):
        keywords = (keywords, )
    f = (lambda x: not x) if exclusive else (lambda x: x)
    entries = [entry for entry in feed['entries'] if f(any(keyword in entry['title'] for keyword in keywords))]
    filtered_feed = copy.copy(feed)
    filtered_feed.entries = entries
    return filtered_feed
print('loading original feed')
feed = feedparser.parse(url_feed_929)
print('done')

def enclosure(entry):
    return next(
            PyRSS2Gen.Enclosure(
                url = link.href,
                length = link.length,
                type = link.type
            )
            for link in entry.links 
            if link.rel == 'enclosure'
            )


def feed_to_rss(parsed_feed, title):
    items = [
            PyRSS2Gen.RSSItem(
                title = x.title,
                link = x.link,
                description = x.summary,
                author = x.author,
                enclosure = enclosure(x),
                guid = x.link,
                pubDate = datetime.datetime(
                    x.published_parsed.tm_year,
                    x.published_parsed.tm_mon,
                    x.published_parsed.tm_mday,
                    x.published_parsed.tm_hour,
                    x.published_parsed.tm_min,
                    x.published_parsed.tm_sec,
                    ))
                for x in parsed_feed.entries
                ]
    rss = PyRSS2Gen.RSS2(
            title = title,
            link = parsed_feed['feed'].get("link"),
            description = parsed_feed['feed'].get("description"),

            language = parsed_feed['feed'].get("language"),
            copyright = parsed_feed['feed'].get("copyright"),
            managingEditor = parsed_feed['feed'].get("managingEditor"),
            webMaster = parsed_feed['feed'].get("webMaster"),
            pubDate = parsed_feed['feed'].get("pubDate"),
            lastBuildDate = parsed_feed['feed'].get("lastBuildDate"),
            image = PyRSS2Gen.Image(  # todo: use item image
                url = parsed_feed.entries[0].image.href,
                title = title,
                link = parsed_feed['feed'].get("image").get("link"),
                ),
            categories = parsed_feed['feed'].get("categories"),
            generator = parsed_feed['feed'].get("generator"),
            docs = parsed_feed['feed'].get("docs"),

            items = items
            )
    return rss

# todo: set another title to feed
def filter_by_keyword(feed, keywords, filename, title=None, exclusive=False):
    if not title and isinstance(keywords, basestring):
        title = keywords
    elif not title:
        raise ValueError('please set a title')
    filtered_feed = filter_feed(feed, keywords, exclusive)
    rss = feed_to_rss(filtered_feed, '929 - ' + title)
    rss.write_xml(open('feeds/929-' + filename + '.rss', 'wb'))

print('generate feeds')
filter_by_keyword(feed, u'929 פרקים למחשבה', 'daily-chapter', 'הפרק היומי', exclusive=True)
filter_by_keyword(feed, u'הרב בני לאו', 'harav-benny-lau')
filter_by_keyword(feed, u'הרב דוד מנחם', 'harav-david-menachem')
filter_by_keyword(feed, u'מקריא את', 'omer-frenkel-makri')
filter_by_keyword(feed, u'תקציר', 'taktzir')
filter_by_keyword(feed, u'התכנית 929 פרקים למחשבה', 'full-929-lemachsava', u'פרקים למחשבה - תכניות מלאות')
filter_by_keyword(feed, u'בתכנית 929 פרקים למחשבה', 'short-929-lemachsava', u'פרקים למחשבה - קטעים')
filter_by_keyword(feed, u'מושג ישראלי', 'musag', u'מושג ישראלי')
filter_by_keyword(feed, [u'929 פרקים למחשבה', u'הרב בני לאו', u'הרב דוד מנחם', u'מקריא את', u'תקציר'], 'other', u'עוד על הפרק היומי')
print('done')
