"""Util that calls SAP."""
from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any, Dict, List, Optional

import requests
from langchain_core.pydantic_v1 import BaseModel, Extra, root_validator
from langchain_core.utils import get_from_dict_or_env

# class Coupon():
#     def __init__(self, active, id, name, startDate, endDate) -> None:
#         self.active = active
#         self.id = id
#         self.name = name
#         self.startDate = startDate
#         self.endDate = endDate

class SAPAPIWrapper(BaseModel):
    """Wrapper for SAP API."""

    api_url: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    token: Optional[str] = None

    class Config:
        """Configuration for this pydantic object."""
        extra = Extra.forbid

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that api key and python package exists in environment."""
        
        api_url = get_from_dict_or_env(values, "api_url", "API_URL")

        client_id = get_from_dict_or_env(
            values, "client_id", "CLIENT_ID"
        )

        client_secret = get_from_dict_or_env(
            values, "client_secret", "CLIENT_SECRET"
        )

        payload = {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret
        }
        response = requests.post(api_url + '/authorizationserver/oauth/token', data=payload, verify=False)

        if response.status_code == 200:
            token = response.json()['access_token']
        else:
            raise ValueError(
                "Failed to get access token."
            )
        values["api_url"] = api_url
        values["client_id"] = client_id
        values["client_secret"] = client_secret
        values["token"] = token
        return values

    def create_coupon(self, coupon: dict):
        header = {}
        header["Authorization"] = 'bearer ' + self.token
        header["Content-Type"]='application/xml'
        body='<?xml version="1.0" encoding="UTF-8"?>' \
        '<singleCodeCoupon>' \
        f'<active>{coupon["active"]}</active>' \
        f'<couponId>{coupon["id"]}</couponId>' \
        '<maxRedemptionsPerCustomer>1</maxRedemptionsPerCustomer>' \
        '<maxTotalRedemptions>1</maxTotalRedemptions>' \
        f'<name>{coupon["name"]}</name>' \
        f'<startDate>{coupon["startDate"]}</startDate>' \
        f'<endDate>{coupon["endDate"]}</endDate>' \
        '</singleCodeCoupon>'
        response = requests.post(self.api_url + '/couponwebservices/couponservices/v2/singlecodecoupon/create', headers=header, data=body, verify=False)
        return response.json()

    def run(self, mode: str, coupon: dict):
        print("***"*10)
        print(coupon)
        # if mode == "create_coupon":
        #     return json.dumps(self.create_coupon(coupon))


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    sap = SAPAPIWrapper()
    # new_coupon = Coupon("true", "testabc4", "testabc4", "2020-09-27T19:23:51Z", "2026-12-27T19:23:51Z")
    new_coupon = {
        "active": "true",
        "id": "testabc4",
        "name": "testabc4",
        "startDate": "2020-09-27T19:23:51Z",
        "endDate": "2026-12-27T19:23:51Z"
    }
    result = sap.run("create_coupon", new_coupon)
    print(result)