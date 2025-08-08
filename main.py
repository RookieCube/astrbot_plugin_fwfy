import json
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger

@register("message_translator", "Cici", "监听消息并进行搞笑翻译", "1.0.0")
class MessageTranslator(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.event_message_type("ALL")
    async def translate_all_messages(self, event: AstrMessageEvent):
        """监听所有消息，进行搞笑翻译 (谨慎使用!)"""
        try:
            content = event.message_str
            # Safety check: Ignore messages from the bot itself
            if event.is_from_self():
                return

            # Safety check: Ignore commands (prevent infinite loops)
            if content.startswith("/"):
                return

            # Limit the length of the message to avoid overloading the LLM
            if len(content) > 200:
                yield event.plain_result("消息过长，无法翻译。")
                return

            llm_response = await self.context.get_using_provider().text_chat(
                prompt=f"请用'狗屁不通'的逐词直译方式翻译：{content}",
                contexts=[],
                image_urls=[],
                func_tool=None,
                system_prompt="你是一个翻译助手，请将输入文本进行逐词直译，并使翻译结果尽可能的'狗屁不通'且搞笑。"
            )

            if llm_response.role == "assistant":
                result = llm_response.completion_text.strip()
                yield event.plain_result(result)
            else:
                yield event.plain_result("翻译出错：LLM返回了非助手角色的回复。")

        except Exception as e:
            logger.error(f"翻译出错: {e}")
            yield event.plain_result(f"翻译出错: {e}")
