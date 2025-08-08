import json
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger

@register("all_message_processor", "Cici", "处理所有消息的插件", "1.0.0")
class AllMessageProcessor(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.event_message_type("ALL")
    async def on_all_message(self, event: AstrMessageEvent):
        """处理所有消息事件 (谨慎使用!)"""
        try:
            content = event.message_str

            # Safety check: Ignore messages from the bot itself
            if event.is_from_self():
                return

            # Safety check: Ignore commands (prevent infinite loops)
            if content.startswith("/"):
                return

            # Limit message length to avoid overloading the LLM
            if len(content) > 200:
                yield event.plain_result("消息过长，无法处理。")
                return


            # Process the message content here...
            # Example:  Send the message content back to the user with a prefix
            processed_message = f"你发送了：{content}"
            yield event.plain_result(processed_message)

        except Exception as e:
            logger.error(f"处理消息出错: {e}")
            yield event.plain_result(f"处理消息出错: {e}")
