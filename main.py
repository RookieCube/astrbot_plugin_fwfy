from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register

@register("fwfy_translator", "Cici", "一个逐词直译的搞笑翻译插件", "1.0.0")
class FwfyTranslator(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.command("fwfy")
    async def translate(self, event: AstrMessageEvent, content: str):
        """
        逐词直译翻译，输出搞笑翻译结果。
        """
        try:
            words = content.split()
            translated_words = []
            for word in words:
                llm_response = await self.context.get_using_provider().text_chat(
                    prompt=f"请直译单词：{word}",
                    contexts=[],
                    image_urls=[],
                    func_tool=None,
                    system_prompt="你是一个翻译助手，请只返回单词的直译。"
                )
                if llm_response.role == "assistant":
                    translated_words.append(llm_response.completion_text.strip())
                else:
                    translated_words.append(f"无法翻译：{word}")

            result = " ".join(translated_words)
            yield event.plain_result(result)

        except Exception as e:
            yield event.plain_result(f"翻译出错: {e}")
