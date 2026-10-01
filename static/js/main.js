// Client-side interactions for Smart Recruitment System
document.addEventListener('DOMContentLoaded', function () {
    
    // Auto dismiss flash alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Client-side File Upload validation (10MB max & allowed extensions)
    const fileInputs = document.querySelectorAll('input[type="file"][name="resume"]');
    fileInputs.forEach(function (input) {
        input.addEventListener('change', function () {
            if (this.files && this.files[0]) {
                const file = this.files[0];
                const fileSizeMB = file.size / (1024 * 1024);
                const allowedExtensions = ['pdf', 'doc', 'docx'];
                const fileName = file.name;
                const fileExt = fileName.split('.').pop().toLowerCase();

                if (fileSizeMB > 10) {
                    alert('File size exceeds the 10MB maximum limit. Please select a smaller file.');
                    this.value = '';
                    return;
                }

                if (!allowedExtensions.includes(fileExt)) {
                    alert('Invalid file format! Only PDF, DOC, and DOCX files are allowed.');
                    this.value = '';
                    return;
                }
            }
        });
    });

    // Password Match Validation on Register
    const registerForm = document.querySelector('form[action*="register"]');
    if (registerForm) {
        registerForm.addEventListener('submit', function (e) {
            const pass = registerForm.querySelector('input[name="password"]').value;
            const confirmPass = registerForm.querySelector('input[name="confirm_password"]').value;

            if (pass !== confirmPass) {
                e.preventDefault();
                alert('Passwords do not match. Please verify your entries.');
            }
        });
    }

    // Modal action binder for job deletion
    const deleteModal = document.getElementById('deleteConfirmModal');
    if (deleteModal) {
        deleteModal.addEventListener('show.bs.modal', function (event) {
            const button = event.relatedTarget;
            const jobId = button.getAttribute('data-job-id');
            const jobTitle = button.getAttribute('data-job-title');
            
            const modalTitleSpan = deleteModal.querySelector('#deleteJobTitleSpan');
            const deleteForm = deleteModal.querySelector('#deleteJobForm');
            
            if (modalTitleSpan) modalTitleSpan.textContent = jobTitle;
            if (deleteForm) deleteForm.action = '/recruiter/delete-job/' + jobId;
        });
    }
});
