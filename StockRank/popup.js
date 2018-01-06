//https://stockpredictor.herokuapp.com/?symbol=GOOGL&compname=GOOGLE
$(document).ready(function() {

$('#shoot').click(function(){
	//get the data from this API and print in the popup.html table
  $.ajax({url: "http://127.0.0.1:5000/?symbol="+document.getElementById('symbol').value, success: function(result){
  console.log(result)
  document.getElementById('displayTable').style.display="block";
  $("#company").html(document.getElementById('symbol').value);
  $("#prediction").html(result['val']);
  $("#rank").html(result['rank']);

},error: function(xhr, error){
        console.log(xhr); 
		console.log(error);
 }});
})

});