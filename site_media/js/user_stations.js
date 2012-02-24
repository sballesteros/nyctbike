$(function () {

    //where the map is centered
    var mylat = 40.757108;
    var mylng = -73.98188;
    var myzoom = 11;
    var mydiv = 'map_canvas'; //in which div do we put the map

    var serveDataDjango = '/serve_stations_data_user/'

    var myusername = $("#username_for_mapit").html(); //some tag with this ID

    //what happen when we click on a marker whose title is stationId
     function myFuncOnMarkerClick(marker, myid) {
	 var stationId = marker.title;
	 window.location.replace('/stations/?id='+ stationId);	  
    }
    
    mapit(mylat, mylng, myzoom, mydiv, myFuncOnMarkerClick, serveDataDjango, false, myusername);

});
