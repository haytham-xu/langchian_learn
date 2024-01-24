"""SAP Toolkit."""
from typing import Dict, List

from langchain_core.pydantic_v1 import BaseModel, Field

from langchain_community.agent_toolkits.base import BaseToolkit
from langchain_community.tools import BaseTool
from tools.coupon.prompt import (
    CREATE_COUPON,
)
from tools.coupon.tool import SAPAction
from utilities.coupon import SAPAPIWrapper


class NoInput(BaseModel):
    """Schema for operations that do not require any input."""

    no_input: str = Field("", description="No input required, e.g. `` (empty string).")

class Coupon(BaseModel):
    # TODO Counpon schema
    active: str = Field(description="the coupon's status, true or false, true means this coupon would be valid, false means this coupon is expired")
    id: str = Field(description="the coupon's id, it should be unique")
    name: str = Field(description="the coupon's name, it should contain commodity name")
    startDate: str = Field(description="the coupon's begining date, it should be format like 2020-09-27T19:23:51Z")
    endDate: str = Field(description="the coupon's end date, it should be format like 2020-09-27T19:23:51Z")

class SAPToolkit(BaseToolkit):
    """SAP Toolkit.
    """

    tools: List[BaseTool] = []

    # TODO Tools generator
    @classmethod
    def from_sap_api_wrapper(
        cls, sap_api_wrapper: SAPAPIWrapper
    ) -> "SAPToolkit":
        operations: List[Dict] = [
            {
                "mode": "create_coupon",
                "name": "Create Coupon",
                "description": CREATE_COUPON,
                "args_schema": Coupon,
            },
        ]
        tools = [
            SAPAction(
                name=action["name"],
                description=action["description"],
                mode=action["mode"],
                api_wrapper=sap_api_wrapper,
                args_schema=action.get("args_schema", None),
            )
            for action in operations
        ]
        return cls(tools=tools)

    def get_tools(self) -> List[BaseTool]:
        """Get the tools in the toolkit."""
        return self.tools
