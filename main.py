from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register

@register("fwfy_translator_listener", "RookieCube", "一个监听所有消息并进行搞笑翻译的插件", "1.0.0")
class FwfyTranslatorListener(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.event_message_type(filter.EventMessageType.ALL)
    async def translate_all_messages(self, event: AstrMessageEvent):
        """
        监听所有消息，进行逐词直译搞笑翻译。
        """
        try:
            message_str = event.message_str.strip()
            # 分割命令和内容
            parts = message_str.split(maxsplit=1)

            if not parts or parts[0] != "fwfy":
                return  # 非触发命令直接返回

            if len(parts) < 2:
                yield event.plain_result("🐾 请在后边输入要翻译的内容~")
                return

            text_to_translate = parts[1]

            llm_response = await self.context.get_using_provider().text_chat(
                prompt=f"请用狗屁不通的逐词直译方式翻译：{text_to_translate}",
                contexts=[],
                image_urls=[],
                func_tool=None,
                system_prompt="你是一个翻译助手，请将输入文本进行人机搞笑翻译，并使翻译结果尽可能的'狗屁不通',使用一词的别的意思而不是该语境的正确意思（相当于逐词翻译然后连起来成一句话，不要有空格）。"
            )

            if llm_response.role == "assistant":
                result = llm_response.completion_text.strip()
                yield event.plain_result(f"{result}")
            else:
                yield event.plain_result("翻译出错：LLM返回了非助手角色的回复。")

        except Exception as e:
            yield event.plain_result(f"翻译出错：{str(e)}")
