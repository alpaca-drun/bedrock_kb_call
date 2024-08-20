from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import boto3
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Boto3 클라이언트 설정
bedrock_agent_runtime = boto3.client(
    service_name='bedrock-agent-runtime',
    region_name='us-east-1',
    endpoint_url='https://bedrock-agent-runtime.us-east-1.amazonaws.com'
)

# 템플릿 설정
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

class InputModel(BaseModel):
    text: str

@app.post("/retrieve")
def retrieve(input: InputModel):
    kbId = ''
    modelArn = 'arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0'

    system_prompt = ''
    full_prompt = system_prompt + '\n\n' + input.text

    try:
        response = bedrock_agent_runtime.retrieve_and_generate(
            input={
                'text': full_prompt,
            },
            retrieveAndGenerateConfiguration={
                'knowledgeBaseConfiguration': {
                    "generationConfiguration": {
                        "inferenceConfig": {
                            "textInferenceConfig": {
                                "maxTokens": 4000,
                                "temperature": 0.5,
                                "topP": 0.5
                            }
                        },
                    },
                    'knowledgeBaseId': kbId,
                    'modelArn': modelArn
                },
                'type': 'KNOWLEDGE_BASE'
            }
        )
        output = response["output"]
        return {"text": output['text']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
