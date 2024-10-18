from flask import Flask, request, render_template, send_file
from graphviz import Digraph
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.form['data']
    generate_flowchart(data)
    return send_file('static/flowchart.png', mimetype='image/png')

def generate_flowchart(data):
    dot = Digraph()

    lines = data.split('\n')
    for line in lines:
        if '->' in line:
            edge_parts = line.split('->')
            for i in range(len(edge_parts) - 1):
                dot.edge(edge_parts[i].strip(), edge_parts[i+1].strip())
        elif ':' in line:
            # Handle node definition with shape
            node, shape = line.split(':')
            dot.node(node.strip(), shape=shape.strip())
        else:
            # Handle standard node without shape
            dot.node(line.strip())

    dot.render('static/flowchart', format='png', cleanup=True)

if __name__ == '__main__':
    app.run(debug=True)