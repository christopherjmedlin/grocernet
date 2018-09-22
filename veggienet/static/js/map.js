mapboxgl.accessToken = 'pk.eyJ1IjoiY2hyaXN0b3BoZXJqbWVkbGluIiwiYSI6ImNqbTg2ajdmaTAxanAzcW1oeW1zNng0c2cifQ.Zki78qEgErytwYY4-TM1tQ';

var map = new mapboxgl.Map({
    container: "map-container",
    style: "mapbox://styles/christopherjmedlin/cjm88j5zo5fax2rpby5517ge0"
});

var markerReq = new XMLHttpRequest();
markerReq.addEventListener("load", function() {
    points = JSON.parse(this.responseText)["vendors"];
    for (var point in points) {
        new mapboxgl.Marker()
            .setLngLat(points[point])
            .addTo(map);
    }
});

markerReq.open("GET", "/api/v1/vendors/?points_only=True");
markerReq.send();
