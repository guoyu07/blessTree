/**
 * Created by albert on 16-1-28.
 */
$(function () {

    //玩?
    $("#pg_11-rej").on('tap', function () {
        //alert("success");
        $("#black-mask").show();
        $("#tips-container").show();
    })
    $("#pg_11-plant").on('tap', function () {
        location.href="http://localhost:63342/tree/templates/pg_12.html?first=1&pass=success"
        //alert("success");
    })

    //不玩时候
    $("#selected-sure").on('tap', function () {
        alert("happy new year");
        $("#black-mask").hide();
        $("#tips-container").hide();
    })
    $("#selected-not").on('tap', function(){
        $("#black-mask").hide();
        $("#tips-container").hide();
    })

})