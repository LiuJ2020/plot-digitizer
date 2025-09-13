document.addEventListener('DOMContentLoaded', function() {
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
        
        // Display original image
        originalImage.src = `data:image/jpeg;base64,${result.image_data}`;
        
        // Display info about extracted points
        const pointCount = result.results.point_count;
        dataPointsInfo.innerHTML = `
            <strong>Found ${pointCount} data points</strong><br>
            <small>Points are automatically detected from the plot image and converted to coordinates.</small>
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
            coordinatesTable.innerHTML = '<p class="text-muted">No data points detected. Try adjusting the axis ranges or use a clearer image.</p>';
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
        
        const csvContent = 'X,Y\n' + 
            currentData.results.coordinates
                .map(point => `${point[0]},${point[1]}`)
                .join('\n');
        
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
        
        const textContent = 'X\tY\n' + 
            currentData.results.coordinates
                .map(point => `${point[0]}\t${point[1]}`)
                .join('\n');
        
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
});