import json
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger

@register("fwfy_translator", "Cici", "飞舞人机翻译插件", "1.0.0")
class FwfyTranslator(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.command("fwfy") # Use @filter.command for command handling
    async def translate(self, event: AstrMessageEvent, content: str):
        """飞舞人机翻译"""
        try:
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
