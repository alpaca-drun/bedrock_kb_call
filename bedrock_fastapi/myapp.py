from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import boto3

app = FastAPI()

bedrock_agent_runtime = boto3.client(
    service_name='bedrock-agent-runtime',
    region_name='us-east-1',
    endpoint_url='https://bedrock-agent-runtime.us-east-1.amazonaws.com'
)

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
