"""On-page SEO checks for the static site (stdlib only).

Run: python3 -m unittest discover -s tests
"""

import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path

PUBLIC = Path(__file__).resolve().parent.parent / "public"
SITE = "https://mesure-du-temps.julsql.fr"
NOT_INDEXED = {"404.html"}


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.lang = None
        self.title = ""
        self.meta = {}
        self.links = {}
        self.headings = []
        self.images = []
        self.jsonld = []
        self._in = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.lang = a.get("lang")
        elif tag == "title":
            self._in = "title"
        elif tag == "meta" and ("name" in a or "property" in a):
            self.meta[a.get("name") or a.get("property")] = a.get("content", "")
        elif tag == "link":
            self.links[a.get("rel")] = a.get("href")
        elif re.fullmatch(r"h[1-6]", tag):
            self.headings.append(int(tag[1]))
        elif tag == "img":
            self.images.append(a)
        elif tag == "script" and a.get("type") == "application/ld+json":
            self._in = "jsonld"
            self.jsonld.append("")

    def handle_endtag(self, tag):
        if tag in ("title", "script"):
            self._in = None

    def handle_data(self, data):
        if self._in == "title":
            self.title += data
        elif self._in == "jsonld":
            self.jsonld[-1] += data


def url_for(rel):
    path = "/" + rel
    return SITE + (path[: -len("index.html")] if path.endswith("index.html") else path)


def parse(path):
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


PAGES = sorted(p.relative_to(PUBLIC).as_posix() for p in PUBLIC.rglob("*.html"))
INDEXED = [p for p in PAGES if p not in NOT_INDEXED]


class SeoTest(unittest.TestCase):
    def test_sitemap_lists_every_public_page(self):
        sitemap = (PUBLIC / "sitemap.xml").read_text(encoding="utf-8")
        locs = set(re.findall(r"<loc>(.*?)</loc>", sitemap))
        self.assertEqual(locs, {url_for(p) for p in INDEXED})

    def test_titles_and_descriptions_are_unique(self):
        pages = [parse(PUBLIC / p) for p in PAGES]
        titles = [p.title for p in pages]
        descriptions = [p.meta.get("description") for p in pages]
        self.assertEqual(len(set(titles)), len(titles))
        self.assertEqual(len(set(descriptions)), len(descriptions))

    def test_common_tags(self):
        for rel in PAGES:
            with self.subTest(page=rel):
                p = parse(PUBLIC / rel)
                self.assertEqual(p.lang, "fr")
                self.assertTrue(50 <= len(p.title) <= 60, f"title length {len(p.title)}")
                desc = p.meta.get("description", "")
                self.assertTrue(140 <= len(desc) <= 160, f"description length {len(desc)}")
                self.assertIn("theme-color", p.meta)
                self.assertTrue((PUBLIC / p.links["icon"].lstrip("/")).is_file())
                self.assertTrue((PUBLIC / p.links["apple-touch-icon"].lstrip("/")).is_file())

    def test_headings(self):
        for rel in PAGES:
            with self.subTest(page=rel):
                levels = parse(PUBLIC / rel).headings
                self.assertEqual(levels.count(1), 1)
                self.assertEqual(levels[0], 1)
                for prev, cur in zip(levels, levels[1:]):
                    self.assertLessEqual(cur, prev + 1, f"heading jump h{prev} -> h{cur}")

    def test_images_have_alt_and_dimensions(self):
        for rel in PAGES:
            for img in parse(PUBLIC / rel).images:
                with self.subTest(page=rel, img=img.get("src")):
                    self.assertIn("alt", img)
                    self.assertIn("width", img)
                    self.assertIn("height", img)

    def test_indexed_pages_social_and_structured_data(self):
        for rel in INDEXED:
            with self.subTest(page=rel):
                p = parse(PUBLIC / rel)
                url = url_for(rel)
                self.assertEqual(p.links.get("canonical"), url)
                self.assertEqual(p.meta.get("og:url"), url)
                for key in ("og:title", "og:description", "og:type", "twitter:card"):
                    self.assertTrue(p.meta.get(key), key)
                image = p.meta.get("og:image", "")
                self.assertTrue(image.startswith(SITE + "/assets/images/"), image)
                self.assertTrue((PUBLIC / image[len(SITE) + 1 :]).is_file(), image)
                self.assertEqual(p.meta.get("twitter:image"), image)
                self.assertTrue(p.jsonld, "missing JSON-LD")
                for block in p.jsonld:
                    self.assertEqual(json.loads(block)["@context"], "https://schema.org")

    def test_404_is_not_indexed(self):
        p = parse(PUBLIC / "404.html")
        self.assertEqual(p.meta.get("robots"), "noindex")
        self.assertNotIn("canonical", p.links)


if __name__ == "__main__":
    unittest.main()
