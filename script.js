
document.getElementById('insuranceForm').addEventListener('submit', function (e) {
    e.preventDefault();
    const formData = Object.fromEntries(new FormData(e.target).entries());

    fetch('http://localhost:5000/generate-pdf', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => {
        if (!response.ok) throw new Error("Server error");
        return response.blob();
    })
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = "insurance_form.pdf";
        document.body.appendChild(a);
        a.click();
        a.remove();
    })
    .catch(error => {
        alert("שגיאה ביצירת קובץ ה-PDF");
        console.error(error);
    });
});
