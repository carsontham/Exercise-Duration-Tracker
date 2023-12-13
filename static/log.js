function postdata() {

    var datetime_input = $ ('.datetime_input').val();
    var weight = $ ('.log_weight_input').val();
    var walking = $ ('.walking_input').val();
    var running = $ ('.running_input').val();
    var swimming = $ ('.swimming_input').val();
    var bicycling = $ ('.bicycling_input').val();


    $.ajax({
    
    url: "http://127.0.0.1:5000/log",
    method: "POST",
    data:{
        datetime: datetime_input,
        weight: weight,
        walking: walking,
        running: running,
        swimming: swimming,
        bicycling: bicycling,
        }
    }).done(function(data) {
        $('.output_space h2').html(data.cal) 
    }
    )
};
