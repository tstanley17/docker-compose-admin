from flask import Flask, render_template, request, redirect, url_for, session
import os
import subprocess
from docker import DockerClient
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key
client = DockerClient(base_url='unix://var/run/docker.sock')

@app.route('/')
def home():
    directory = session.get('compose_directory', None)
    compose_files = None
    if directory and os.path.exists(directory):
        compose_files = []
        for root, _, files in os.walk(directory):
            for f in files:
                if f in ('docker-compose.yml', 'docker-compose.yaml'):
                    file_path = os.path.join(root, f)
                    relative_dir = os.path.relpath(root, directory) if root != directory else '.'
                    stack_name = os.path.basename(root) if root != directory else os.path.splitext(f)[0]
                    compose_files.append({
                        'filename': f,
                        'file_path': file_path,
                        'directory': relative_dir,
                        'stack_name': stack_name
                    })
    return render_template('home.html', directory=directory, compose_files=compose_files)

@app.route('/set_directory', methods=['POST'])
def set_directory():
    directory = request.form.get('directory')
    if directory and os.path.isdir(directory):
        session['compose_directory'] = directory
        return redirect(url_for('home'))
    else:
        return "Invalid directory", 400

@app.route('/browse_files', methods=['GET', 'POST'])
def browse_files():
    current_dir = request.args.get('path', os.path.expanduser('~'))
    if not os.path.isdir(current_dir):
        current_dir = os.path.expanduser('~')
    
    if request.method == 'POST':
        selected_file = request.form.get('selected_file')
        if selected_file and os.path.isfile(selected_file) and os.path.basename(selected_file) in ('docker-compose.yml', 'docker-compose.yaml'):
            session['compose_directory'] = os.path.dirname(selected_file)
            return redirect(url_for('home'))
    
    directories = []
    files = []
    try:
        for item in os.listdir(current_dir):
            item_path = os.path.join(current_dir, item)
            if os.path.isdir(item_path):
                directories.append(item)
            elif os.path.isfile(item_path) and item in ('docker-compose.yml', 'docker-compose.yaml'):
                files.append(item)
        
        parent_dir = os.path.dirname(current_dir) if current_dir != os.path.expanduser('~') else None
        return render_template('browse.html', 
                             current_dir=current_dir, 
                             directories=sorted(directories), 
                             files=sorted(files), 
                             parent_dir=parent_dir)
    except Exception as e:
        return f"Error accessing directory: {e}", 500

@app.route('/compose/<path:filename>')
def view_compose(filename):
    directory = session.get('compose_directory')
    if not directory:
        return "Directory not set", 400
    file_path = os.path.join(directory, filename)
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            content = f.read()
        return render_template('edit_compose.html', filename=filename, content=content)
    else:
        return "File not found", 404

@app.route('/save_compose/<path:filename>', methods=['POST'])
def save_compose(filename):
    directory = session.get('compose_directory')
    if not directory:
        return "Directory not set", 400
    file_path = os.path.join(directory, filename)
    content = request.form.get('content')
    try:
        with open(file_path, 'w') as f:
            f.write(content)
        return redirect(url_for('view_compose', filename=filename))
    except Exception as e:
        return f"Error saving file: {e}", 500

@app.route('/up/<path:filename>', methods=['POST'])
def up(filename):
    directory = session.get('compose_directory')
    if not directory:
        return "Directory not set", 400
    file_path = os.path.join(directory, filename)
    try:
        subprocess.run(
            ['docker', 'compose', '-f', os.path.basename(filename), 'up', '-d'],
            cwd=os.path.dirname(file_path),
            check=True
        )
        return "Stack started"
    except subprocess.CalledProcessError as e:
        return f"Failed to start stack: {e}", 500

@app.route('/down/<path:filename>', methods=['POST'])
def down(filename):
    directory = session.get('compose_directory')
    if not directory:
        return "Directory not set", 400
    file_path = os.path.join(directory, filename)
    try:
        subprocess.run(
            ['docker', 'compose', '-f', os.path.basename(filename), 'down'],
            cwd=os.path.dirname(file_path),
            check=True
        )
        return "Stack stopped"
    except subprocess.CalledProcessError as e:
        return f"Failed to stop stack: {e}", 500

@app.route('/pull/<path:filename>', methods=['POST'])
def pull(filename):
    directory = session.get('compose_directory')
    if not directory:
        return "Directory not set", 400
    file_path = os.path.join(directory, filename)
    try:
        subprocess.run(
            ['docker', 'compose', '-f', os.path.basename(filename), 'pull'],
            cwd=os.path.dirname(file_path),
            check=True
        )
        return "Images pulled successfully"
    except subprocess.CalledProcessError as e:
        return f"Failed to pull images: {e}", 500

@app.route('/status/<path:filename>')
def status(filename):
    directory = session.get('compose_directory')
    if not directory:
        return "Directory not set", 400
    file_path = os.path.join(directory, filename)
    project_name = os.path.basename(os.path.dirname(file_path))
    containers = client.containers.list(all=True, filters={"label": f"com.docker.compose.project={project_name}"})
    status_info = [{'name': container.name, 'status': container.status} for container in containers]
    return render_template('status.html', filename=filename, status_info=status_info)

if __name__ == '__main__':
    app.run(port=5802, debug=True)