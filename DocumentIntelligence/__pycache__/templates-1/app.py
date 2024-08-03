from flask import Flask, render_template, request

import boto3

app = Flask(__name__, template_folder='C:\\DocumentIntelligence\\templates')


# Configure Kendra client
kendra_client = boto3.client('kendra', region_name='us-east-1')  # Replace 'us-east-1' with your AWS region
index_id = 'acd6e4ef-afe7-4fb2-8ec8-b5dcfe3de742'  # Replace 'your_index_id' with your Amazon Kendra index ID

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    response = kendra_client.query(
        QueryText=query,
        IndexId=index_id
    )
    # Process response and display search results
    results = []
    for item in response['ResultItems']:
        results.append({
            'DocumentId': item['DocumentId'],
            'DocumentTitle': item['DocumentTitle']['Text'],
            'DocumentExcerpt': item['DocumentExcerpt']['Text']
        })
    return render_template('result.html', results=results)

if __name__ == '__main__':
    app.run(debug=True, port=5000)