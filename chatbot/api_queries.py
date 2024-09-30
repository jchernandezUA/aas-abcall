import random
from base import app, api
from flask_restful import Resource

class ChatbotList(Resource):
    def get(self):
        return [{
            "id": "1000",
            "user": 10,
            "start": "Mon 23 2024 23:20:15",
            "end": "Mon 23 2024 23:20:15",
            "total_messages": 120
        }]
    

api.add_resource(ChatbotList, '/chatbot')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002, use_reloader=False)


