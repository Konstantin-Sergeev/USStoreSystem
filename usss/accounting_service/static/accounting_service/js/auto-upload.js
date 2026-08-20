window.addEventListener('load', function() {
    const activeForm = document.getElementById('file-form');
    document.getElementById('file-input').addEventListener('change', function() {
        if (this.files.length > 0) {
            const formData = new FormData(activeForm);
            fetch (activeForm.action, {'method' : 'POST', 'body' : formData})
        }
    })
});