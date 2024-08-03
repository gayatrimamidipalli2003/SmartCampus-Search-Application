from flask import Flask, request, render_template
import subprocess
import json

app = Flask(__name__)

def run_aws_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout
        else:
            return f"Error executing command: {result.stderr}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

def format_result(json_str):
    try:
        result_dict = json.loads(json_str)
        if 'ResultItems' in result_dict:
            lines = []
            for item in result_dict['ResultItems']:
                if 'DocumentExcerpt' in item:
                    excerpt = item['DocumentExcerpt']['Text']
                    lines.append(excerpt) 
                    # Append the whole excerpt as a line
            return lines
        else:
            return ["No results found."]
    except Exception as e:
        return [f"Error formatting result: {str(e)}"]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query_text = request.form['query_text']
        index_id = "acd6e4ef-afe7-4fb2-8ec8-b5dcfe3de742"
        aws_command = f'aws kendra query --index-id "{index_id}" --query-text "{query_text}"'
        output = run_aws_command(aws_command)
        formatted_output = format_result(output)
        return render_template('index.html', query=query_text, output=formatted_output)
    return render_template('index.html', output=None)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

