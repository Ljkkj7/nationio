let autocomplete = {};

fetch(AUTOCOMPLETE_URL)
    .then(res => res.json())
    .then(data => {
        autocomplete = data;
    });

document.getElementById("guess").addEventListener("input", function () {
    let lookupStr = this.value;

    for (let country of autocomplete[lookupStr[0].toLowerCase()]) {
        if (country.startsWith(lookupStr)) {
            console.log(country)
        }
    }
});