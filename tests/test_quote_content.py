import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch
from urllib.parse import urlparse

from extended_content import IQTIBOSLAR, format_iqtibos, get_random_iqtibos_item
from gemini_content import _prompt
from main import content_selected, daily_broadcast


class QuoteBankTests(unittest.TestCase):
    def test_each_quote_has_a_valid_source_and_distinct_text(self):
        self.assertGreaterEqual(len(IQTIBOSLAR), 10)
        self.assertEqual(
            len({item["matn"] for item in IQTIBOSLAR}),
            len(IQTIBOSLAR),
        )
        for item in IQTIBOSLAR:
            with self.subTest(author=item["muallif"], source=item["manba"]):
                self.assertTrue(item["matn"].strip())
                self.assertTrue(item["muallif"].strip())
                self.assertTrue(item["manba"].strip())
                parsed = urlparse(item["url"])
                self.assertEqual(parsed.scheme, "https")
                self.assertTrue(parsed.netloc)

    def test_random_quote_can_skip_previously_used_text(self):
        first_text = IQTIBOSLAR[0]["matn"]
        for _ in range(30):
            self.assertNotEqual(
                get_random_iqtibos_item(exclude_texts={first_text})["matn"],
                first_text,
            )

    def test_formatted_quote_includes_author_and_work(self):
        item = IQTIBOSLAR[0]
        text = format_iqtibos(item)
        self.assertIn(item["matn"], text)
        self.assertIn(item["muallif"], text)
        self.assertIn(item["manba"], text)

    def test_quote_generation_is_not_available_in_gemini_prompts(self):
        with self.assertRaises(ValueError):
            _prompt("iqtibos", None)


class QuoteHandlerTests(unittest.IsolatedAsyncioTestCase):
    async def test_quote_button_uses_local_quote_and_source_link(self):
        item = IQTIBOSLAR[0]
        query = SimpleNamespace(
            data="content:iqtibos",
            answer=AsyncMock(),
            edit_message_text=AsyncMock(),
        )
        store = Mock()
        context = SimpleNamespace(
            bot=SimpleNamespace(send_chat_action=AsyncMock()),
            application=SimpleNamespace(bot_data={"store": store}),
        )
        update = SimpleNamespace(
            callback_query=query,
            effective_chat=SimpleNamespace(id=123),
        )

        with (
            patch("main.get_random_iqtibos_item", return_value=item),
            patch("main.generate_gemini_content", new_callable=AsyncMock) as generate,
        ):
            await content_selected(update, context)

        generate.assert_not_awaited()
        call = query.edit_message_text.await_args
        self.assertIn(item["matn"], call.args[0])
        self.assertIn(item["muallif"], call.args[0])
        source_button = call.kwargs["reply_markup"].inline_keyboard[0][0]
        self.assertEqual(source_button.url, item["url"])

    async def test_daily_quote_is_local_and_has_a_source_link(self):
        item = IQTIBOSLAR[0]
        store = SimpleNamespace(
            active_users=lambda: [{"chat_id": 123}],
            upsert=Mock(),
            set_active=Mock(),
        )
        bot = SimpleNamespace(send_message=AsyncMock())
        application = SimpleNamespace(bot_data={"store": store}, bot=bot)

        with (
            patch("main.random.choice", return_value="iqtibos"),
            patch("main.get_random_iqtibos_item", return_value=item),
            patch("main.generate_gemini_content", new_callable=AsyncMock) as generate,
        ):
            await daily_broadcast(application)

        generate.assert_not_awaited()
        sent = bot.send_message.await_args.kwargs
        self.assertIn(item["matn"], sent["text"])
        source_button = sent["reply_markup"].inline_keyboard[0][0]
        self.assertEqual(source_button.url, item["url"])


if __name__ == "__main__":
    unittest.main()
