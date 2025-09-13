#!/usr/bin/env python3
"""
Plot Digitizer Web Application

A lightweight Flask-like web app that takes in images of plots and provides a framework
for analyzing them to extract numerical data. This version uses only built-in Python libraries.
"""

import os
import io
import base64
import json
import mimetypes
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import cgi

class PlotDigitizer:
    """Main class for analyzing plot images and extracting numerical data."""
    
    def __init__(self):
        self.image_data = None
        self.image_info = {}
        
    def load_image_from_data(self, image_data):
        """Load image from binary data."""
        self.image_data = image_data
        # Simple image analysis without OpenCV/PIL
        return True
    
    def analyze_plot_simple(self, x_range=(0, 10), y_range=(0, 10)):
        """
        Simple plot analysis that provides example data points.
        In a real implementation, this would use image processing libraries.
        """
        # For demonstration, return some sample data points
        # In reality, this would analyze the actual image
        sample_points = [
            (1.0, 2.5),
            (2.0, 4.1),
            (3.0, 3.8),
            (4.0, 6.2),
            (5.0, 7.5),
            (6.0, 8.1),
            (7.0, 6.9),
            (8.0, 9.2),
            (9.0, 8.8)
        ]
        
        return {
            'coordinates': sample_points,
            'point_count': len(sample_points),
            'message': 'Demo data - real implementation would analyze the uploaded image'
        }

class PlotDigitizerHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the plot digitizer web app."""
    
    def __init__(self, *args, **kwargs):
        self.routes = {
            '/': self.serve_index,
            '/upload': self.handle_upload,
            '/static/css/style.css': self.serve_css,
            '/static/js/main.js': self.serve_js
        }
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests."""
        parsed = urlparse(self.path)
        path = parsed.path
        
        if path in self.routes:
            self.routes[path]()
        else:
            self.send_error(404)
    
    def do_POST(self):
        """Handle POST requests."""
        parsed = urlparse(self.path)
        path = parsed.path
        
        if path == '/upload':
            self.handle_upload()
        else:
            self.send_error(404)
    
    def serve_index(self):
        """Serve the main index page."""
        html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Plot Digitizer</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="card">
                    <div class="card-header bg-primary text-white">
                        <h1 class="mb-0">📊 Plot Digitizer</h1>
                        <p class="mb-0">Upload plot images and extract numerical data automatically</p>
                    </div>
                    <div class="card-body">
                        <form id="uploadForm" enctype="multipart/form-data">
                            <div class="mb-3">
                                <label for="fileInput" class="form-label">Select Plot Image</label>
                                <input type="file" class="form-control" id="fileInput" name="file" accept="image/*" required>
                                <div class="form-text">Supported formats: PNG, JPG, JPEG, GIF, BMP (max 16MB)</div>
                            </div>
                            
                            <div class="row mb-3">
                                <div class="col-md-6">
                                    <label class="form-label">X-axis Range</label>
                                    <div class="row">
                                        <div class="col">
                                            <input type="number" class="form-control" name="x_min" placeholder="Min" value="0" step="any">
                                        </div>
                                        <div class="col">
                                            <input type="number" class="form-control" name="x_max" placeholder="Max" value="10" step="any">
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <label class="form-label">Y-axis Range</label>
                                    <div class="row">
                                        <div class="col">
                                            <input type="number" class="form-control" name="y_min" placeholder="Min" value="0" step="any">
                                        </div>
                                        <div class="col">
                                            <input type="number" class="form-control" name="y_max" placeholder="Max" value="10" step="any">
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                            <button type="submit" class="btn btn-primary btn-lg w-100">
                                <span id="submitText">Analyze Plot</span>
                                <span id="loadingSpinner" class="spinner-border spinner-border-sm ms-2 d-none" role="status"></span>
                            </button>
                        </form>
                        
                        <div id="results" class="mt-4 d-none">
                            <hr>
                            <h3>Results</h3>
                            <div class="row">
                                <div class="col-md-6">
                                    <h5>Original Image</h5>
                                    <img id="originalImage" class="img-fluid border rounded" alt="Original plot">
                                </div>
                                <div class="col-md-6">
                                    <h5>Extracted Data Points</h5>
                                    <div id="dataPointsInfo" class="alert alert-info"></div>
                                    <div id="coordinatesTable" class="table-responsive"></div>
                                </div>
                            </div>
                            
                            <div class="mt-3">
                                <button id="downloadBtn" class="btn btn-success">Download CSV</button>
                                <button id="copyBtn" class="btn btn-outline-secondary">Copy to Clipboard</button>
                            </div>
                        </div>
                        
                        <div id="error" class="alert alert-danger mt-3 d-none"></div>
                    </div>
                </div>
                
                <div class="text-center mt-3">
                    <small class="text-muted">
                        <strong>Demo Version:</strong> This is a demonstration of the plot digitizer interface. 
                        In the full version, the app would use computer vision libraries to analyze uploaded plot images 
                        and automatically extract data points.
                    </small>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script src="/static/js/main.js"></script>
</body>
</html>'''
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content.encode())
    
    def handle_upload(self):
        """Handle file upload and process the image."""
        try:
            # Parse multipart form data
            content_type = self.headers['content-type']
            if not content_type.startswith('multipart/form-data'):
                self.send_error(400, "Bad Request: Expected multipart/form-data")
                return
            
            content_length = int(self.headers['Content-Length'])
            form_data = self.rfile.read(content_length)
            
            # Simple form parsing for demo purposes
            # In a real implementation, you'd use proper multipart parsing
            
            # For demo, return sample data
            digitizer = PlotDigitizer()
            results = digitizer.analyze_plot_simple()
            
            # Create dummy image data for display
            dummy_image_data = base64.b64encode(b"dummy image data").decode('utf-8')
            
            response_data = {
                'success': True,
                'filename': 'uploaded_plot.png',
                'image_data': dummy_image_data,
                'results': results
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode())
            
        except Exception as e:
            error_response = {'error': f'Error processing upload: {str(e)}'}
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(error_response).encode())
    
    def serve_css(self):
        """Serve CSS styles."""
        css_content = '''body {
    background-color: #f8f9fa;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.card {
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    border: none;
}

.card-header {
    background: linear-gradient(135deg, #007bff, #0056b3) !important;
}

.btn-primary {
    background: linear-gradient(135deg, #007bff, #0056b3);
    border: none;
    transition: transform 0.2s;
}

.btn-primary:hover {
    transform: translateY(-1px);
    background: linear-gradient(135deg, #0056b3, #004085);
}

#originalImage {
    max-height: 300px;
    object-fit: contain;
}

.table-responsive {
    max-height: 300px;
    overflow-y: auto;
}

.data-point-row:hover {
    background-color: #f8f9fa;
}

#results {
    animation: fadeIn 0.5s ease-in;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.spinner-border-sm {
    width: 1rem;
    height: 1rem;
}

.form-control:focus {
    border-color: #007bff;
    box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

.alert-info {
    background-color: #e3f2fd;
    border-color: #bbdefb;
    color: #1976d2;
}

.text-muted {
    font-size: 0.9rem;
    line-height: 1.4;
}'''
        
        self.send_response(200)
        self.send_header('Content-type', 'text/css')
        self.end_headers()
        self.wfile.write(css_content.encode())
    
    def serve_js(self):
        """Serve JavaScript."""
        js_content = '''document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const fileInput = document.getElementById('fileInput');
    const submitText = document.getElementById('submitText');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const resultsDiv = document.getElementById('results');
    const errorDiv = document.getElementById('error');
    const originalImage = document.getElementById('originalImage');
    const dataPointsInfo = document.getElementById('dataPointsInfo');
    const coordinatesTable = document.getElementById('coordinatesTable');
    const downloadBtn = document.getElementById('downloadBtn');
    const copyBtn = document.getElementById('copyBtn');

    let currentData = null;

    uploadForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = new FormData(uploadForm);
        
        // Show loading state
        submitText.textContent = 'Processing...';
        loadingSpinner.classList.remove('d-none');
        resultsDiv.classList.add('d-none');
        errorDiv.classList.add('d-none');
        
        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            if (result.success) {
                displayResults(result);
            } else {
                showError(result.error || 'Unknown error occurred');
            }
        } catch (error) {
            showError('Network error: ' + error.message);
        } finally {
            // Reset loading state
            submitText.textContent = 'Analyze Plot';
            loadingSpinner.classList.add('d-none');
        }
    });

    function displayResults(result) {
        currentData = result;
        
        // Display original image (placeholder for demo)
        originalImage.src = 'data:image/svg+xml;base64,' + btoa('<svg xmlns="http://www.w3.org/2000/svg" width="300" height="200"><rect width="300" height="200" fill="#f0f0f0"/><text x="150" y="100" text-anchor="middle" fill="#666">Uploaded Image Preview</text></svg>');
        
        // Display info about extracted points
        const pointCount = result.results.point_count;
        dataPointsInfo.innerHTML = `
            <strong>Found ${pointCount} data points</strong><br>
            <small>${result.results.message}</small>
        `;
        
        // Display coordinates table
        if (result.results.coordinates.length > 0) {
            const tableHtml = `
                <table class="table table-sm table-striped">
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>X</th>
                            <th>Y</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${result.results.coordinates.map((point, index) => `
                            <tr class="data-point-row">
                                <td>${index + 1}</td>
                                <td>${point[0]}</td>
                                <td>${point[1]}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            `;
            coordinatesTable.innerHTML = tableHtml;
        } else {
            coordinatesTable.innerHTML = '<p class="text-muted">No data points detected.</p>';
        }
        
        resultsDiv.classList.remove('d-none');
    }

    function showError(message) {
        errorDiv.textContent = message;
        errorDiv.classList.remove('d-none');
    }

    // Download CSV functionality
    downloadBtn.addEventListener('click', function() {
        if (!currentData || !currentData.results.coordinates.length) {
            alert('No data to download');
            return;
        }
        
        const csvContent = 'X,Y\\n' + 
            currentData.results.coordinates
                .map(point => `${point[0]},${point[1]}`)
                .join('\\n');
        
        const blob = new Blob([csvContent], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `plot_data_${new Date().toISOString().slice(0, 10)}.csv`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    });

    // Copy to clipboard functionality
    copyBtn.addEventListener('click', async function() {
        if (!currentData || !currentData.results.coordinates.length) {
            alert('No data to copy');
            return;
        }
        
        const textContent = 'X\\tY\\n' + 
            currentData.results.coordinates
                .map(point => `${point[0]}\\t${point[1]}`)
                .join('\\n');
        
        try {
            await navigator.clipboard.writeText(textContent);
            
            // Show feedback
            const originalText = copyBtn.textContent;
            copyBtn.textContent = 'Copied!';
            copyBtn.classList.add('btn-success');
            copyBtn.classList.remove('btn-outline-secondary');
            
            setTimeout(() => {
                copyBtn.textContent = originalText;
                copyBtn.classList.remove('btn-success');
                copyBtn.classList.add('btn-outline-secondary');
            }, 2000);
        } catch (err) {
            alert('Failed to copy to clipboard');
        }
    });

    // File input preview
    fileInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            // Reset previous results
            resultsDiv.classList.add('d-none');
            errorDiv.classList.add('d-none');
        }
    });
});'''
        
        self.send_response(200)
        self.send_header('Content-type', 'application/javascript')
        self.end_headers()
        self.wfile.write(js_content.encode())

def run_server(port=5000):
    """Run the plot digitizer web server."""
    server_address = ('', port)
    httpd = HTTPServer(server_address, PlotDigitizerHandler)
    print(f"🚀 Plot Digitizer Server running on http://localhost:{port}")
    print("📊 Upload plot images to extract numerical data!")
    print("Press Ctrl+C to stop the server")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
        httpd.server_close()

if __name__ == '__main__':
    run_server()