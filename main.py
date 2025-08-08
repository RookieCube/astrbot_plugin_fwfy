import json
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register

@register("fwfy_translator_listener", "Cici", "一个监听所有消息并进行搞笑翻译的插件", "1.0.0")
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
            if message_str == "/fwfy":
                llm_response = await self.context.get_using_provider().text_chat(
                    prompt=f"请用狗屁不通的逐词直译方式翻译：{content}",
                    contexts=[],
                    image_urls=[],
                    func_tool=None,
                    system_prompt="你是一个翻译助手，请将输入文本进行逐词直译，并使翻译结果尽可能的'狗屁不通'（相当于逐词翻译然后连起来）。请忽略开头的/fwfy。"
                )
    
                if llm_response.role == "assistant":
                    result = llm_response.completion_text.strip()
                    yield event.plain_result(result)
                else:
                    yield event.plain_result(f"翻译出错：LLM返回了非助手角色的回复。")
    
        except Exception as e:
            yield event.plain_result(f"翻译出错: {e}")
