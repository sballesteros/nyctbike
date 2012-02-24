var map;
var markersArray = []; //in order to be able to delete the marker we keep track of all the markers added
var imageAlert = MEDIA_URL+'pict/google_bike_red.png';

//ajax the server to get this info
var lat=40.757108;
var lng=-73.98188;

function initialize() {
    var latlng = new google.maps.LatLng(lat, lng);

    var myOptions = {
	zoom: 14,
	center: latlng,
	mapTypeId: google.maps.MapTypeId.ROADMAP
    };

    map = new google.maps.Map(document.getElementById("map_canvas"),
			      myOptions);

    google.maps.event.addListener(map, 'click', function(event) {
	placeMarker(event.latLng);
    });

}

function clearOverlays() {
    //clear the markers
    if (markersArray) {
	for (i in markersArray) {
	    markersArray[i].setMap(null);
	}
    }
}


function placeMarker(location) {
    clearOverlays(); //first clear previous marker

    //add the new one
    var marker = new google.maps.Marker({
	position: location, 
        icon: imageAlert,//image is var image = '{{ MEDIA_URL }}pict/beachflag.png';
	map: map
    });
    //keep track of this new marker
    markersArray.push(marker);

    //alert(location);
    // $("#seb").html(location.toString() )
    //    $("#lat").html(location.lat());
    //    $("#lon").html(location.lng());
    $("#id_latitude").val(location.lat());
    $("#id_longitude").val(location.lng());

    //$.post("/savetrial/", $("#dialog-save").serialize());
}


$(function () {

    initialize();

});

