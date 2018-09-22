initMap = function() {
    var map = L.map('map-container')
    map.setView([51, -0.09])
    map.setZoom(10)
    map.setMaxBounds(L.bounds(50, 100));
    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        id: "mapbox.streets",
        accessToken: "pk.eyJ1IjoiY2hyaXN0b3BoZXJqbWVkbGluIiwiYSI6ImNqbTg2ajdmaTAxanAzcW1oeW1zNng0c2cifQ.Zki78qEgErytwYY4-TM1tQ"
    }).addTo(map);

    var markerReq = new XMLHttpRequest();
    markerReq.addEventListener("load", function() {
        vendors = JSON.parse(this.responseText)["vendors"];

        for (var vendor in vendors) {
            vendor = vendors[vendor]
            markerIcon = document.createElement('i');
            markerIcon.className = "marker-icon"
            /*
            switch (vendor["vendor_type"]) {
                case "store":
                    markerIcon.className += " fas fa-shopping-cart";
                    break;
                case "market":
                    markerIcon.className += " fas fa-store";
                    break;
                case "farm":
                    markerIcon.className += " fas fa-leaf";
                    break;
                default:
                    markerIcon.className += " fas fa-map-marker";
            }
            */
            new L.marker([vendor["location"][1], vendor["location"][0]]).addTo(map)
        }
    });

    markerReq.open("GET", "/api/v1/vendors/");
    markerReq.send();
}

initMap();
