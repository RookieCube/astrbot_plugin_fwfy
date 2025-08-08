from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register

@register("astrbot_plugin_robot_translate", "RookieCube", "一个监听所有消息并进行搞笑翻译的插件", "1.0.1")
class FwfyTranslatorListener(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.event_message_type(filter.EventMessageType.ALL)
    async def translate_all_messages(self, event: AstrMessageEvent, *args):
        """
        监听所有消息，进行逐词直译搞笑翻译。
        """
        try:
            message_str = event.message_str.strip()
            # 分割命令和内容
            parts = message_str.split(maxsplit=2)
            if not parts or parts[0] not in ["robot_translate", "normal_translate"]:
                return
            elif parts[0] == "robot_translate":
                if len(parts) < 3:
                    yield event.plain_result("请在命令后输入目标语言(chi/eng)和要翻译的内容")
                    return

                target_lang = parts[1].lower()
                text_to_translate = parts[2]

                if target_lang not in ["chi", "eng"]:
                    yield event.plain_result("目标语言只能是 chi(中文) 或 eng(英文)")
                    return

                target_lang_text = "中文" if target_lang == "chi" else "英文"
                
                llm_response = await self.context.get_using_provider().text_chat(
                    prompt=f"请将以下内容翻译成{target_lang_text}，使用机翻方式([]内是需翻译内容)：[{text_to_translate}]，请将输入文本进行人机一样的机翻翻译，请使用词的别的意思而不是该语境的正确意思（相当于逐词翻然后连起来成一句话，且不使用该语境下的正确意思，输出{target_lang_text}结果时中间不要有空格，保留可能有的emoji）请不要使用音译。仅输出翻译内容，不要解析翻译内容。",
                    contexts=[],
                    image_urls=[],
                    func_tool=None,
                    system_prompt="你是一个人机翻译助手"
                )

                if llm_response.role == "assistant":
                    result = llm_response.completion_text.strip()
                    yield event.plain_result(f"翻译(人机)为{target_lang_text}的内容：\n{result}")
                else:
                    yield event.plain_result("翻译出错：LLM返回了非助手角色的回复。")
            elif parts[0] == "normal_translate":
                if len(parts) < 3:
                    yield event.plain_result("请在命令后输入目标语言(chi/eng)和要翻译的内容")
                    return

                target_lang = parts[1].lower()
                text_to_translate = parts[2]

                if target_lang not in ["chi", "eng"]:
                    yield event.plain_result("目标语言只能是 chi(中文) 或 eng(英文)")
                    return

                target_lang_text = "中文" if target_lang == "chi" else "英文"

                llm_response = await self.context.get_using_provider().text_chat(
                    prompt=f"请将以下内容翻译成{target_lang_text}([]内是需翻译内容)：[{text_to_translate}]，请使用正确，可信度高，达到原文意思，标准的翻译方法。部分情况下可意译。输出{target_lang_text}时中间不要有空格，保留可能有的emoji。请不要使用音译。仅输出翻译内容。",
                    contexts=[],
                    image_urls=[],
                    func_tool=None,
                    system_prompt="你是一个翻译助手"
                )

                if llm_response.role == "assistant":
                    result = llm_response.completion_text.strip()
                    yield event.plain_result(f"翻译(正常)为{target_lang_text}的内容：{result}")
                else:
                    yield event.plain_result("翻译出错：LLM返回了非助手角色的回复。")
        except Exception as e:
            yield event.plain_result(f"翻译出错：{str(e)}")
