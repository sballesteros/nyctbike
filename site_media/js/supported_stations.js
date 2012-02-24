$(function () {


    //where the map is centered
    var mylat=40.757108;
    var mylng=-73.98188;
    var mydiv = 'map_canvas'; //in which div do we put the map
    var myzoom = 12;
    var serveDataDjango = '/serve_stations_data_supported/'


    //what happen when we click on a marker whose title is stationId
    function myFuncOnMarkerClick(marker, myid) {	

	window.location.replace('/stations?id='+myid);	  

    };
    
    mapit(mylat, mylng, myzoom, mydiv, myFuncOnMarkerClick, serveDataDjango, true, false, 'all');

});
