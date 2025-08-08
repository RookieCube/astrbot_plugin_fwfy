import asyncio
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
@register("fwfy_translator_listener", "RookieCube", "一个监听所有消息并进行搞笑翻译的插件", "1.0.0")
class FwfyTranslatorListener(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.on_startswith("fwfy")
    async def translate_all_messages(self, event: AstrMessageEvent):
        """
        监听所有以 'fwfy' 开头的消息，进行逐词直译搞笑翻译。
        """
        message_str = event.message_str.strip()
        parts = message_str.split(maxsplit=1)
        if len(parts) < 2:
            yield event.plain_result("🐾 请在后边输入要翻译的内容~")
            return
        
        text_to_translate = parts[1]
        try:
            llm_response = await self.context.get_using_provider().text_chat(
                prompt=f"请用狗屁不通的逐词直译方式翻译：{text_to_translate}",
                contexts=[],
                image_urls=[],
                func_tool=None,
                system_prompt="你是一个翻译助手，请将输入文本进行人机搞笑翻译，并使翻译结果尽可能的'狗屁不通'（相当于逐词翻译然后连起来成一句话，不要有空格）。"
            )
            if llm_response.role == "assistant":
                result = llm_response.completion_text.strip()
                yield event.plain_result(f"{result}")
            else:
                yield event.plain_result("翻译出错：LLM返回了非助手角色的回复。")
        except asyncio.TimeoutError as error:
            yield event.plain_result("翻译服务出现了超时问题，请稍后再试~")
            logger.error(f"翻译插件超时: {error}", exc_info=error)
