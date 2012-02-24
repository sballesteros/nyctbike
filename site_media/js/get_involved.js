$(function () {

    $('.button_detail').show()

    $(".button_detail").click(function() {
	var id = $(this).attr('id').split('_')[1];
	if($(this).val() == 'see details')
	{
	    $("#content_"+id).show()	
	    $("#details_"+id).val('hide details')	
	}
	else{
	    $("#content_"+id).hide()	
	    $("#details_"+id).val('see details')	
	}
    });
    
});
