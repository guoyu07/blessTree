/**
 * Created by albert on 15-12-7.
 */
/**
 * Created by albert on 15-11-29.
 */

$(function () {

    init_main();


    /****
     * 微信js-sdk接口认证
     * */

    wx.config({
        debug:true,
        appId:'',
        timestamp:'',
        nonceStr:'',
        signature:'',
        jsApiList:[]
    })

    /*********************
     * 点击事件，按钮
     * */
    //积分按钮


    //排行按钮


    //心愿按钮
    $(".willing").fadeIn(1000)
        .on('tap', function () {
            $.ajax({
                type:'POST'
            });
            $(".weui_dialog_hd").html('<p>这是心愿</p>');
            $("#dialog1").show();
            $("#dialog1").find('.weui_btn_dialog').on('tap', function(){
                $("#dialog1").hide();
            })
        })
    //.ajax({
    //    type:'POST',
    //});

    //添加朋友按钮
    $("#add_friend").fadeIn(1300)
        .on('tap', function () {

        })

    $('.rank').fadeIn(1600)
        .on('tap', function(){

        })

    //浇水按钮
    $(".water-flower").fadeIn(1000)
        .on('tap', function () {
            $(".list-contain").hide();
            $(".tree-img").fadeIn();
            $(".bless-tucao").fadeIn();
        });

    //历史按钮
    $(".history").fadeIn(1300)
        .on('tap', function () {
            //$.ajax({
            //    type:'POST',
            //    //TODO 请求服务器的数据
            //})
            $(".my_mask").show();
            $(".weui_icon_cancel").on('tap', function () {
                    $('.list-contain').fadeOut();
                    $(".my_mask").hide();
                    $(".tree-img").show();
                    $(".bless-tucao").show();
            });
            $(".tree-img").hide();
            $(".bless-tucao").hide();
            $(".list-contain").fadeIn();
        });

    //$(".weui_mask").on('tap', function () {
    //    $(this).hide();
    //})

    $('.tips').fadeIn(1600)
        .on('tap', function () {

        })

    //颜色变化动画效果
    //function enphaze(){
    //    $(".tips").animate({
    //        "background-color":"#7FFF00"
    //    }, 1000);
    //};
    //
    //setInterval(enphaze, 1000);

    //祝福按钮
    $(".bless").on('tap', function () {
        $(".weui_dialog_hd").html('<p>这是祝福</p>');
        $("#dialog1").show();
        $("#dialog1").find('.weui_btn_dialog').on('tap', function(){
            $("#dialog1").hide();
        })
    })


    //吐槽按钮
    $(".tucao").on('tap', function () {
        $(".weui_dialog_hd").html('<p>这是吐槽</p>');
        $("#dialog1").show();
        $("#dialog1").find('.weui_btn_dialog').on('tap', function(){
            $("#dialog1").hide();
        })
    })


    /********************
     * 一些函数
     * */
    function init_main(){
        //$('.menu-top').css(
        //    "height",($(window).height()*0.2).toString()
        //);
        //alert("test")
        $(".tree-img").fadeIn();
        $(".bless-tucao").fadeIn();
        var windowheight = ($(window).height()-$('.menu-top').height());
        $('.container').css(
            "height",(windowheight*0.95).toString()
        );

        $('.footer').css(
            "height",(windowheight*0.05).toString()
        )
        //$('.bless-tocao').css(
        //    "top",(windowheight*0.8).toString()
        //)
    };
})
