from flask import Flask, request, render_template, send_from_directory, flash, redirect, url_for
import os
import re
import subprocess

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pcap', 'pcapng'}
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10 MB limit
app.secret_key = 'supersecretkey'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def run_tshark(pcap_file, protocol, num_matches):
    # Command to run tshark to get TCP/UDP conversations
    tshark_command = ['tshark', '-n', '-q', '-r', pcap_file, '-z', f'conv,{protocol.lower()}']

    # Run the tshark command and capture the output 
    process = subprocess.run(tshark_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    # Extract output from tshark
    tshark_output = process.stdout

    # Regular expression to match lines with IP addresses and ports
    pattern = re.compile(r'(\d+\.\d+\.\d+\.\d+)(?::(\d+))?\s+<->\s+(\d+\.\d+\.\d+\.\d+)(?::(\d+))?')

    # Find all matches in the tshark output
    matches = pattern.findall(tshark_output)

    # Process only the specified number of matches
    filters = []
    for idx, match in enumerate(matches[:num_matches], 1):  # Limit to specified number of matches
        ip1, port1 = match[0], match[1]
        ip2, port2 = match[2], match[3]
        
        # Build the filter string conditionally
        filter_parts = []
        
        filter_parts.append(f"ip.addr=={ip1}")
        if port1:
            filter_parts.append(f"{protocol.lower()}.port=={port1}")
        filter_parts.append(f"ip.addr=={ip2}")
        if port2:
            filter_parts.append(f"{protocol.lower()}.port=={port2}")
    
        filter_string = ' && '.join(filter_parts)
        filters.append((filter_string, idx))
        
    a=[]
    output_files = []
    # Loop through each filter and write the output to a separate pcap file
    for filter_string, idx in filters:
        output_pcap = os.path.join(app.config['UPLOAD_FOLDER'], f'filtered_stream_{idx}.pcap')
        tshark_filter_command = [
            'tshark', '-r', pcap_file, '-Y', filter_string, '-w', output_pcap
        ]
        # Run the tshark command to apply the filter and write to the new pcap file
        subprocess.run(tshark_filter_command)
        output_files.append(f'filtered_stream_{idx}.pcap')
        a.append(len(filter_parts))

    return None, output_files

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        protocol = request.form['protocol']
        num_matches = int(request.form['num_matches'])

        error, output_files = run_tshark(os.path.join(app.config['UPLOAD_FOLDER'], filename), protocol, num_matches)

        if error:
            flash(error)
            return redirect(request.url)

        return render_template('results.html', files=output_files)

    else:
        flash('Invalid File provided. Submit valid PCAP file')
        return redirect(request.url)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
