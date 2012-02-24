$(function () {

/*POST the profile form. the div within the table was impossible to replace so we resend the table tag. Don't understand why have to do this*/

    $( '#button_save_profile' ).click(function() {
	$.post("/form_profile_ajax/", $("#form_profile").serialize(), function(data){
            var myobj = eval(data);
	    if(myobj.form_ok){
		$("#wtf").remove();
		$('#replace_profile').html('<table id="wtf">'+myobj.html+'</table>');
		$('#error_profile').html("");
		$('#button_save_profile').val("data saved").css("background-color", "green");
		$('#button_save_profile').delay(2000).queue(function(){
		    $(this).val("Save").css("background-color", "black");
		    $(this).dequeue();
		});

		if(myobj.form_uncomplete){
		    $('.alert').css("color", "red");
		    $('.alert').html('You need to complete your full profile to be able to submit/support ideas');
		}
		else{
		    $('.alert').css("color", "green");
		    $('.alert').html('Your profile is complete, you can submit/support ideas');
		    $('#button_save_profile').remove();
		    $('#remove_me').remove();
		    $('#myactions').html('<a class="add_station" href="/submitstation?next=/stations">Submit a stations</a> <a class="add_designstation" href="/submitdesignstation?next=/designstations">Submit a station Design</a> <a class="add_designbike" href="/submitdesignbike?next=/designbikes">Submit a bike Design</a> <a class="add_idea" href="/submitidea?next=/ideas">Submit an idea</a>');
		}

	    }
	    else{
		$('#error_profile').html("Your profile has not been updated, please correct the errors");
		$('#replace_profile').html('<table id="wtf">'+myobj.html+'</table>');
	    }
	});
    });

})