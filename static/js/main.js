document.addEventListener('DOMContentLoaded', function() {
    // Weather detection logic will be implemented here
});

// Live city autocomplete using GeoDB Cities API
document.addEventListener('DOMContentLoaded', function() {
    const cityInput = document.getElementById('city-input');
    const suggestionBox = document.createElement('div');
    suggestionBox.setAttribute('id', 'city-suggestions');
    suggestionBox.style.position = 'absolute';
    suggestionBox.style.background = '#fff';
    suggestionBox.style.border = '1px solid #ccc';
    suggestionBox.style.zIndex = '1000';
    suggestionBox.style.width = cityInput.offsetWidth + 'px';
    suggestionBox.style.maxHeight = '180px';
    suggestionBox.style.overflowY = 'auto';
    suggestionBox.style.display = 'none';
    cityInput.parentNode.appendChild(suggestionBox);

    cityInput.addEventListener('input', function() {
        const value = cityInput.value.trim();
        if (value.length < 2) {
            suggestionBox.style.display = 'none';
            return;
        }
        // GeoDB Cities API endpoint
        const apiUrl = `https://wft-geo-db.p.rapidapi.com/v1/geo/cities?namePrefix=${encodeURIComponent(value)}&limit=8&sort=-population`;
        fetch(apiUrl, {
            method: 'GET',
            headers: {
                'X-RapidAPI-Key': 'fa0e713d75msh6562a04dc497a39p1ac2f8jsn51ad19e472d0', // Replace with your RapidAPI key
                'X-RapidAPI-Host': 'wft-geo-db.p.rapidapi.com'
            }
        })
        .then(response => response.json())
        .then(data => {
            suggestionBox.innerHTML = '';
            if (data.data && data.data.length > 0) {
                data.data.forEach(cityObj => {
                    const city = cityObj.city;
                    const country = cityObj.country;
                    const item = document.createElement('div');
                    item.textContent = `${city}, ${country}`;
                    item.style.padding = '8px';
                    item.style.cursor = 'pointer';
                    item.addEventListener('mousedown', function(e) {
                        cityInput.value = city;
                        suggestionBox.style.display = 'none';
                    });
                    suggestionBox.appendChild(item);
                });
                suggestionBox.style.display = 'block';
                suggestionBox.style.left = cityInput.offsetLeft + 'px';
                suggestionBox.style.top = (cityInput.offsetTop + cityInput.offsetHeight) + 'px';
            } else {
                suggestionBox.style.display = 'none';
            }
        })
        .catch(() => {
            suggestionBox.style.display = 'none';
        });
    });

    document.addEventListener('click', function(e) {
        if (e.target !== cityInput) {
            suggestionBox.style.display = 'none';
        }
    });
});
