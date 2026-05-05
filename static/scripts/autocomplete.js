let autocomplete = {};

fetch(AUTOCOMPLETE_URL)
    .then(res => res.json())
    .then(data => {
        autocomplete = data;
    });

document.getElementById("guess").addEventListener("input", function () {
    let lookupStr = this.value.toLowerCase();
    document.getElementById("autocomplete-results").innerHTML = "";

    if (lookupStr.length === 0) {
        return;
    }

    for (let country of autocomplete[lookupStr[0]]) {
        if (country.toLowerCase().startsWith(lookupStr)) {
            document.getElementById("autocomplete-results").innerHTML += `<div class="autocomplete-option"><p>${country}</p></div>`;
        }
    }
});