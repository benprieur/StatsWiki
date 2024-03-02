document.addEventListener('DOMContentLoaded', function() {
    var numberElements = document.querySelectorAll('.number');    
    numberElements.forEach(function(element) {
        var number = parseInt(element.textContent, 10);
        
        if (!isNaN(number)) {
            element.textContent = number.toLocaleString('en-US');
        }
    });
});