import logging

from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

from src.settings import get_settings


logger = logging.getLogger(__name__)


class OpenAiLLMService:
    """OpenAI LLM Completion service"""

    def __init__(self, openai_api_key: str | None = None, llm_model: str | None = None):
        self._settings = get_settings()

        self._openai_api_key = openai_api_key or self._settings.OPEN_AI_API_KEY

        self.llm_model = llm_model or self._settings.OPEN_AI_LLM_MODEL
        self.llm = ChatOpenAI(
            api_key=SecretStr(self._openai_api_key),
            model=self.llm_model,
            verbose=True,
            max_retries=self._settings.OPEN_AI_RETRIES,
            timeout=self._settings.OPEN_AI_TIMEOUT,
            temperature=0.0,
            base_url=self._settings.OPEN_AI_PROXY_URL,
        )

    async def ainvoke(self, system_prompt: str, user_input: str) -> str:
        """Async invoke prompt to OpenAI"""

        prompt_template = ChatPromptTemplate(
            input_variables=[],
            messages=[
                SystemMessagePromptTemplate.from_template(system_prompt),
                HumanMessage(user_input),
            ],
        )
        messages = prompt_template.format_messages()

        response = await self.llm.agenerate([messages])
        result = response.generations[0][0].text

        logger.info("LLM response: %s", result)

        return result
