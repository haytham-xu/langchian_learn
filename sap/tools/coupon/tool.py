from typing import Optional, Type, Any

from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.tools import BaseTool

from utilities.coupon import SAPAPIWrapper


class SAPAction(BaseTool):
    """Tool for interacting with the GitHub API."""

    api_wrapper: SAPAPIWrapper = Field(default_factory=SAPAPIWrapper)
    mode: str
    name: str = ""
    description: str = ""
    args_schema: Optional[Type[BaseModel]] = None

    def _run(
        self,
        instructions: Optional[dict] = {},
        run_manager: Optional[CallbackManagerForToolRun] = None,
        **kwargs: Any
    ) -> str:
        return self.api_wrapper.run(self.mode, kwargs)
