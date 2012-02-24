$(function () {


    //where the map is centered
    var mylat=40.757108;
    var mylng=-73.98188;
    var mydiv = 'map_canvas'; //in which div do we put the map
    var myzoom = 12;
    var serveDataDjango = '/serve_stations_data/'


    //what happen when we click on a marker whose title is stationId
    function myFuncOnMarkerClick(marker, myid) {	

	var stationId = marker.title;
	markersArray[previousId].setIcon(imageBase);
	previousId = myid;
	
	marker.setIcon(imageAlert);

	$('#ajax').load('/get_station_info/', 'id=' + stationId);

    };
    
    mapit(mylat, mylng, myzoom, mydiv, myFuncOnMarkerClick, serveDataDjango, true, false, 'all');

});
