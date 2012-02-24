var map;
var markersArray = []; //in order to be able to delete the marker we keep track of all the markers added
var previousId = 0;
var image = '../pict/beachflag.png';


//ajax the server to get this info
var lat=40.757108
var lng=-73.98188

var data= [{"lat": 40.7372997418606, "lng": -73.9833820370483, "title": "1"}, {"lat": 40.7508987419184, "lng": -73.9926088360596, "title": "2"}, {"lat": 40.768159694612, "lng": -73.9817941693115, "title": "3"}, {"lat": 40.724657412956, "lng": -73.9780176190185, "title": "4"}, {"lat": 40.8051126336894, "lng": -73.9391363171387, "title": "5"}];

function initialize() {
    var latlng = new google.maps.LatLng(lat, lng);

    var myOptions = {
	zoom: 12,
	center: latlng,
	mapTypeId: google.maps.MapTypeId.ROADMAP
    };

    map = new google.maps.Map(document.getElementById("map_station"),
			      myOptions);

    var lend=data.length;

    for(var i=0; i<lend; i++) {
	var mylatlng = new google.maps.LatLng(data[i].lat, data[i].lng);
	placeMarker(mylatlng, data[i].title, i);
    }

};

function clearOverlays() {
    //clear the markers
    if (markersArray) {
	for (i in markersArray) {
	    markersArray[i].setMap(null);
	}
    }
};

function placeMarker(location, title, myid) {

//    clearOverlays(); //first clear previous marker

    //add the new one
    var marker = new google.maps.Marker({
	position: location, 
	map: map,
	title: title
    });

    //keep track of this new marker
    markersArray.push(marker);

    google.maps.event.addListener(marker, 'click', function(event) {
	markersArray[previousId].setIcon();
	previousId = myid;
	
	marker.setIcon(image);
    });

};


function toggleCurrentMarker(myid) {

    var i = 0;
    while (markersArray[i].title != myid)
    {
	i++;
    }

    markersArray[i].setIcon(image);
    previousId = i;

};


$(function () {

    initialize();
    toggleCurrentMarker('3');
    

});
