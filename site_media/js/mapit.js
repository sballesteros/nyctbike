var markersArray = []; //in order to be able to delete the marker we keep track of all the markers added
var previousId = 0;
var imageBase = MEDIA_URL+'pict/googlebike5small.png';
var imageAlert = MEDIA_URL+'pict/google_bike_red.png';


function mapit(mylat, mylng, myzoom, mydiv, myFuncOnMarkerClick, serveDataDjango, centerOnData0, myusername)
{
    
    var lat = mylat;
    var lng = mylng;
    var divmap = mydiv;
    
    var map;
    
    var data = [];


    function initialize() {


	var qs = (function(a) {
	    //get query string parameters
	    if (a == "") return {};
	    var b = {};
	    for (var i = 0; i < a.length; ++i)
	    {
		var p=a[i].split('=');
		if (p.length != 2) continue;
		b[p[0]] = decodeURIComponent(p[1].replace(/\+/g, " "));
	    }
	    return b;
	})(window.location.search.substr(1).split('&'));

	if ('id' in qs){
	    $('#ajax').load('/get_station_info/', 'id=' + qs['id']);
	}


	var latlng = new google.maps.LatLng(lat, lng);

	var myOptions = {
	    zoom: myzoom,
	    center: latlng,
	    mapTypeId: google.maps.MapTypeId.ROADMAP
	};

	map = new google.maps.Map(document.getElementById(divmap),
				  myOptions);

	var lend=data.length;

	for(var i=0; i<lend; i++) {
	    var mylatlng = new google.maps.LatLng(data[i].lat, data[i].lng);
	    placeMarker(mylatlng, data[i].title, i);
	    
	    //allow stations.html to display the right station description when called with a querry string parameter id
	    if ('id' in qs){
		if(markersArray[i].title == qs['id'])
		{
		    markersArray[i].setIcon(imageAlert);
		    previousId = i;
		}
	    }

	}

    };


    function placeMarker(location, title, myid)
    {

	//add the new one
	var marker = new google.maps.Marker({
	    position: location, 
	    map: map,
            icon: imageBase,//image is var image = '{{ MEDIA_URL }}pict/beachflag.png';
	    title: title
	});

	
	google.maps.event.addListener(marker, 'click', function(event) {
	    myFuncOnMarkerClick(marker, myid);
	});

	//keep track of this new marker
	markersArray.push(marker);

    };



    function onDataReceived(mydata)
    {
	var myobj = eval(mydata);
	var lend=myobj.length;

	for(var i=0; i<lend; i++) {
	    var myo = myobj[i];
	    data.push(myo);
	}	

	if(centerOnData0)
	{
	    lat = data[0].lat;
	    lng = data[0].lng;
	}

	initialize();
	
    };
    
    $.get(serveDataDjango, 'username=' + myusername, onDataReceived);


};


