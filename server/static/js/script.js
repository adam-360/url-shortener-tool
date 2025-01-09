function shortenUrl() {
    var inputUrl = document.getElementById('full_url').value;
    var formData = new FormData();
    formData.append('url', inputUrl);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '{{ url_for("shorten_url") }}', true);
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

    xhr.onload = function() {
        if (xhr.status === 200) {
            // Display the shortened URL
            var resultContainer = document.getElementById('resultContainer');
            var shortenedUrl = document.getElementById('shortenedUrl');

            shortenedUrl.innerHTML = 'Shortened URL: <a href="' + JSON.parse(xhr.responseText).shortened_url + '" target="_blank">' + JSON.parse(xhr.responseText).shortened_url + '</a>';
            resultContainer.style.display = 'block';

            // Clear the input box for the next URL
            document.getElementById('full_url').value = '';
        } else {
            // Handle errors
            console.error('Error:', xhr.status, xhr.statusText);
        }
    };

    xhr.onerror = function() {
        // Handle errors if needed
        console.error('Request failed');
    };

    // Send the request with the form data
    xhr.send(formData);
}

function pasteFromClipboard() {
    navigator.clipboard.readText().then((text) => {
        document.getElementById('url').value = text;
    }).catch((err) => {
        console.error('Error pasting from clipboard: ', err);
    });
}

function copyToClipboard() {
    var shortenedUrl = document.getElementById('shortened-url').innerHTML;
    navigator.clipboard.writeText(shortenedUrl);

    // Show the tooltip
    var tooltip = document.getElementById('copy-tooltip');
    tooltip.style.visibility = 'visible';
    
    // Hide the tooltip after 2 seconds
    setTimeout(function() {
        tooltip.style.visibility = 'hidden';
    }, 2000);
}