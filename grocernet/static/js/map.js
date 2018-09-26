initMap = function(mapboxToken) {
    var map = L.map('map-container')
    map.setView([0, 0])
    map.setZoom(0)
    map.setMaxBounds(L.bounds(50, 100));
    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        id: "mapbox.streets",
        accessToken: mapboxToken
    }).addTo(map);

    var markerReq = new XMLHttpRequest();

    markerReq.addEventListener("load", function() {
        markers = L.markerClusterGroup()
        vendors = JSON.parse(this.responseText)["vendors"];

        for (var vendor in vendors) {
            vendor = vendors[vendor];
            icon = null;
            
            switch (vendor["vendor_type"]) {
                case "store":
                    icon = "shopping-cart";
                    break;
                case "market":
                    icon = "store";
                    break;
                case "farm":
                    icon = "leaf";
                    break;
                default:
                    icon = null;
            }
            
            markerIcon = L.AwesomeMarkers.icon({
                icon: icon,
                markerColor: "green",
                prefix: "fa"
            });

            marker = new L.marker([vendor["location"][1], vendor["location"][0]],
                {icon: markerIcon})

            vendor_page = "/vendor/" + vendor["id"]
            popup_html = '<a href="' + vendor_page + '">' + vendor["name"] + '</a>'
            marker.bindPopup(popup_html)

            marker.addTo(markers);
        }

        map.addLayer(markers);
    });

    markerReq.open("GET", "/api/v1/vendors/");
    markerReq.send();
}

if (MAPBOX_ACCESS_TOKEN != "") {
    initMap(MAPBOX_ACCESS_TOKEN);
}