import boto3

 

bedrock_agent_runtime = boto3.client(
    service_name='bedrock-agent-runtime',
    region_name='us-east-1',
    endpoint_url='https://bedrock-agent-runtime.us-east-1.amazonaws.com'
)


def retrieve(input):
    kbId = ''
    modelArn = 'arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0'

    system_prompt = ''
    full_prompt = system_prompt + '\n\n' + input
    
    return bedrock_agent_runtime.retrieve_and_generate(
        input={
            'text':full_prompt,
        },
        retrieveAndGenerateConfiguration={
            'knowledgeBaseConfiguration':{
                "generationConfiguration" : {
                        "inferenceConfig":{
                            "textInferenceConfig": {
                                "maxTokens": 4000,
                                "temperature": 0.5,
                                "topP": 0.5
                            }
                        },
                    },
                'knowledgeBaseId': kbId,
                'modelArn':modelArn
                },
            'type':'KNOWLEDGE_BASE'
        }
    )
    
    
event = ''
response = retrieve(event)
output = response["output"]
print(output['text'])
