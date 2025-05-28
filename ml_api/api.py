# ml_api/api.py
import json
import recommendation_model

def handler(event, context):
    body = json.loads(event['body'])
    background = body.get('background')
    goal = body.get('goal')
    experience = body.get('experience')
    path = recommendation_model.recommend_learning_path(background, goal, experience)
    return {
        'statusCode': 200,
        'body': json.dumps({'learning_path': path}),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }