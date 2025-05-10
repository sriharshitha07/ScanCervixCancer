// File: static/js/script.js
document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('file');
    const uploadArea = document.getElementById('upload-area');
    const previewContainer = document.getElementById('preview-container');
    const imagePreview = document.getElementById('image-preview');
    const removeImageBtn = document.getElementById('remove-image');
    
    if (uploadArea) {
        // Handle click on upload area
        uploadArea.addEventListener('click', function() {
            fileInput.click();
        });
        
        // Handle drag & drop
        uploadArea.addEventListener('dragover', function(e) {
            e.preventDefault();
            uploadArea.classList.add('border-primary');
        });
        
        uploadArea.addEventListener('dragleave', function() {
            uploadArea.classList.remove('border-primary');
        });
        
        uploadArea.addEventListener('drop', function(e) {
            e.preventDefault();
            uploadArea.classList.remove('border-primary');
            
            if (e.dataTransfer.files.length) {
                fileInput.files = e.dataTransfer.files;
                updatePreview();
            }
        });
        
        // Handle file input change
        fileInput.addEventListener('change', updatePreview);
        
        // Handle remove image button
        if (removeImageBtn) {
            removeImageBtn.addEventListener('click', function() {
                fileInput.value = '';
                previewContainer.classList.add('d-none');
                uploadArea.classList.remove('d-none');
            });
        }
        
        // Function to update image preview
        function updatePreview() {
            if (fileInput.files && fileInput.files[0]) {
                const reader = new FileReader();
                
                reader.onload = function(e) {
                    imagePreview.src = e.target.result;
                    previewContainer.classList.remove('d-none');
                    uploadArea.classList.add('d-none');
                }
                
                reader.readAsDataURL(fileInput.files[0]);
            }
        }
    }
});