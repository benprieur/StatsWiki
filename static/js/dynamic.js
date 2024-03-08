document.addEventListener('DOMContentLoaded', function() {
    var numberElements = document.querySelectorAll('.number');    
    numberElements.forEach(function(element) {
        var number = parseInt(element.textContent, 10);
        
        if (!isNaN(number)) {
            element.textContent = number.toLocaleString('en-US');
        }
    });
});

function asyncImageLoading(url) {
    fetch(url)
        .then(response => response.blob())
        .then(imageBlob => {
            const imageUrl = URL.createObjectURL(imageBlob);
            document.getElementById('imageAsynchrone').src = imageUrl;
        });
}

document.addEventListener('DOMContentLoaded', (event) => {
    sort_numeric_table(2); 
});
