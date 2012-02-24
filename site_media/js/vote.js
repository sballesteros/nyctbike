$(document).ready(function() {

    function info(myselector, mytext, mycolor){
	$(myselector).html(mytext).css("color", mycolor);
	$(myselector).delay(2000).queue(function(){
	    $(this).html("")
	    $(this).dequeue();
	});
    };

    function myCallback(answer, myinput, type){
        var myobj = eval(answer)

	if(myobj.auth){//if user is authentified we update the vote buttons
	    if(myobj.already){
		var d = new Date(myobj.when);
		info('span.' + type + '_' +myobj.id, 'You already voted "' + myobj.what + '" on ' + d.toLocaleDateString(), 'red');
	    }
	    else{
		var keep = myinput.val();
		myinput.val(keep.split(':')[0]+':'+myobj.nb);
		//	    $('#ajax').load('/get_station_info/', 'id=' + myobj.id);	
		info('span.' + type + '_' +myobj.id, 'Thanks for your vote', 'green');
	    }
	}
	else{//user not identified send him to login page
	    window.location.replace('/accounts/login?next='+myobj.next);	  
	}
    }

    $( 'input[type=button]' ).filter(function(){
	var c = $(this).attr('class');
	return ( c == 'like' ||  c == 'dontcare' ||  c == 'dontlike'); 
    }).click(function() {
	var myinput = $(this);
	var formType = myinput.closest("div").attr("class");
	var type = formType.split('_')[1]

	$.post("/"+formType+"/", myinput.closest("form").serialize(), function(data){
	    myCallback(data, myinput, type);
	});

    });

});





