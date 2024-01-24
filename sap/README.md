# AI-Coupon

## Set Up Environment

```Bash
pip install -r requirements.txt
```

## Set Up Configuration
You need to create `.env` file under root directory. This file contains variables which would be loaded by `load_dotenv` function as environment variables.

In this case, the file should contain llm token, coupon API url, coupon client id and secret. It may look like:
```
GOOGLE_API_KEY=<YOUR_API_TOKEN>

API_URL="https://10.130.226.13:9002"
CLIENT_ID="mobile_android"
CLIENT_SECRET="secret"
```
Here I use google llm, if you use OpenAI token, please change it accordingly.

## Run

```Bash
python main.py
```