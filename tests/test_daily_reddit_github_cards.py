import html
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import daily_reddit_github_cards as cards


class FeedParsingTests(unittest.TestCase):
    def test_extracts_non_stream_chat_completions_envelope(self):
        response = '{"choices":[{"message":{"content":"响应内容"}}]}'
        self.assertEqual(cards.extract_sensenova_content(response, 200, "application/json"), "响应内容")

    def test_parses_sensenova_json_object_items(self):
        content = '{"items":[{"id":7,"name":"工具","description":"中文简介","emoji":"🛠️"}]}'
        self.assertEqual(
            cards.parse_sensenova_summaries(content, {7}),
            {7: {"name": "工具", "description": "中文简介", "emoji": "🛠️"}},
        )

    def test_parses_repo_author_post_time_and_rss_metrics(self):
        post_html = """<div><h1>What it does</h1><p>一个帮助开发者的工具。</p>
        <a href="https://github.com/acme/awesome-tool">https://github.com/acme/awesome-tool</a>
        <h1>Repository stats</h1><table><tr><th>Metric</th><th>Value</th></tr>
        <tr><td>Stars</td><td>1,234</td></tr><tr><td>Forks</td><td>56</td></tr></table></div>"""
        atom = f"""<?xml version="1.0"?><feed xmlns="http://www.w3.org/2005/Atom"><entry>
        <author><name>/u/example_poster</name><uri>https://www.reddit.com/user/example_poster</uri></author>
        <published>2026-10-15T01:00:00+00:00</published><title>Awesome Tool: helpful dev tool (1.2k stars)</title>
        <link href="https://www.reddit.com/r/BestGitHubRepos/comments/abc123/example/" />
        <content type="html">{html.escape(post_html)}</content></entry></feed>""".encode()
        parsed = cards.parse_feed(atom)
        self.assertEqual(len(parsed), 1)
        item = parsed[0]
        self.assertEqual(item.repo_slug, "acme/awesome-tool")
        self.assertEqual(item.author, "example_poster")
        self.assertEqual(item.published, datetime(2026, 10, 15, 1, 0, tzinfo=timezone.utc))
        self.assertEqual(item.metrics, [("Stars", "1,234"), ("Forks", "56")])
        self.assertIn("帮助开发者", item.source_text)

    def test_title_star_metric_fallback(self):
        self.assertEqual(cards.extract_metrics([], "Example Project (5.3k stars)"), [("Stars", "5.3k")])

    def test_latest_duplicate_repo_wins(self):
        older = cards.FeedItem(0, "Old", "https://github.com/acme/tool", "acme/tool", "https://www.reddit.com/r/x/comments/old", "a", "https://www.reddit.com/user/a/", datetime(2026, 10, 14, tzinfo=timezone.utc), [], "old")
        newer = cards.FeedItem(1, "New", "https://github.com/acme/tool", "acme/tool", "https://www.reddit.com/r/x/comments/new", "b", "https://www.reddit.com/user/b/", datetime(2026, 10, 15, tzinfo=timezone.utc), [], "new")
        summaries = {0: {"name": "Tool", "description": "旧帖", "emoji": "📦"}, 1: {"name": "Tool", "description": "新帖", "emoji": "🛠️"}}
        result = cards.newest_unique([older, newer], summaries)
        self.assertEqual([item.reddit_url for item, _ in result], [newer.reddit_url])

    def test_article_has_public_front_matter_links_and_disclaimer(self):
        item = cards.FeedItem(0, "Example", "https://github.com/acme/tool", "acme/tool", "https://www.reddit.com/r/x/comments/abc", "poster", "https://www.reddit.com/user/poster/", datetime(2026, 10, 15, 1, 0, tzinfo=timezone.utc), [("Stars", "1,234")], "summary")
        body = cards.render_article([(item, {"name": "工具", "description": "简短简介", "emoji": "🛠️"})])
        self.assertIn("━━━━━━", cards.render_article([(item, {"name": "工具", "description": "简短简介", "emoji": "🛠️"}), (item, {"name": "工具2", "description": "简介2", "emoji": "📦"})]))
        self.assertIn("Reddit 发帖者", body)
        self.assertIn("RSS 中提供的 GitHub 指标：Stars 1,234", body)
        self.assertIn("未逐项独立核实", body)

    def test_written_post_has_explicit_slug_and_is_public(self):
        item = cards.FeedItem(0, "Example", "https://github.com/acme/tool", "acme/tool", "https://www.reddit.com/r/x/comments/abc", "poster", "https://www.reddit.com/user/poster/", datetime(2026, 10, 15, 1, 0, tzinfo=timezone.utc), [], "summary")
        with tempfile.TemporaryDirectory() as temp_dir:
            path = cards.write_post([(item, {"name": "工具", "description": "简介", "emoji": "📦"})], datetime(2026, 10, 15).date(), Path(temp_dir))
            content = path.read_text(encoding="utf-8")
        self.assertIn('slug: "best-github-repos-2026-10-15"', content)
        self.assertIn("draft: false", content)
        self.assertIn('date: "2026-10-15T10:05:00+08:00"', content)


if __name__ == "__main__":
    unittest.main()
