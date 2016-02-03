/**
 * Created by albert on 16-1-30.
 */
$(function () {

    /****************
     * 初始化
     * */

    var tucao_ran = ['你好丑', '我爱你', '大粗腿', '吨位重', '脚气重']
    var bless_ran = ['你好帅', '真男人', '性感', '四好青年', '怎么吐槽在这？']

    var ran1= $.lqcRandGenerator(5)
    var ran2 = $.lqcRandGenerator(5)
    while(ran1==ran2){
        ran2 = $.lqcRandGenerator(5)
    }
    $("#rand_bless_1").text(bless_ran[ran1]);
    $("#rand_tucao_1").text(tucao_ran[ran1]);
    $("#rand_tucao_2").text(tucao_ran[ran2]);
    $("#rand_bless_2").text(bless_ran[ran2])


    /****************
     * 按钮逻辑
     * */
    //历史按钮
    $("#history").on('tap', function () {

    })


    //历史按钮
    $("#history").on('tap', function () {

    })

    //浇水按钮
    $("#water-flower").on('tap', function () {

    })

    //吐槽
    $("#tucao-btn").on('tap', function () {
        $("#tucao-widget").show();
    })
    $("#tucao-close").on('tap', function () {
        $("tucao-widget").hide();
    })

    $("#rand_tucao_1").on('tap', function () {
        $("#tucao-area").val($('#rand_tucao_1').text())
    })
    $('#rand_tucao_2').on('tap', function () {
        $("#tucao-area").val($('#rand_tucao_2').text())
    })
    //祝福
    $("#bless-btn").on('tap', function () {
        $("#bless-widget").show();
    })
    $("#bless-close").on('tap', function () {
        $("#bless-widget").hide();
    })

    $("#rand_bless_1").on('tap', function () {
        $("#bless-area").val($('#rand_bless_1').text())
    })
    $('#rand_bless_2').on('tap', function () {
        $("#bless-area").val($('#rand_bless_2').text())
    })
    $('#bless_confirm').on('tap', function () {
        var tucao_con = $('#bless-area').val();
        var na = $("#bless-na").is(':checked') //是否匿名

    })
})