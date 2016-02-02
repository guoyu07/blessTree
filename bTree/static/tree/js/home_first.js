/**
 * Created by albert on 15-12-7.
 */
/**
 * Created by albert on 15-11-29.
 */

$(function () {

    /********************
     * 初始化
     * */
    // 一些局部变量
    var myDate = new Date()
    var blesspull = 5;
    var tucaopull = 5;
    var rankpull = 5;
    var msgpull = 5;
    init_main(myDate);
    
    /********************
     * 引导按钮绑定事件
     * */
    //看完规则后按钮
    $('#rule-next').on('tap', function () {
        $('#rule').hide();
        $('#tips-quming').show();
    })

    //提醒取名字
    $('#quming-btn').on('tap', function () {
        $('#tips-quming').hide();
        $("#fill-in-name").show();
    })

    //填写完树名字之后ajax提交到服务器的按钮
    $('#fill-btn').on('tap', function () {
        alert("you click it");
        tree_name = $("#text_id").val();  //获取树的名字
        $.post('http://1.blesstree.sinaapp.com/wechat/ajax',
            {
                'ajax_type': '1',
                'openid': $("#user_message_openid").text(),
                'nickname': $("#user_message_nickname").text(),
                'tree_name': tree_name
            },
            function(ret) {
                if (ret == '1') {
                    alert("提交成功！");
                    $("#whos_tree").html(tree_name);
                } else if (ret == "2") {
                    alert("您的网络有问题，请再试一下哦～");
                } else {
                    alert("网络不太好，请再试一下哦～");
                }
            })
        $("#fill-in-name").hide();
        $("#black-mask").hide();
        $("#tips-water").show();
    })

    $("#water-tips-btn").on('tap', function () {
        $("#tips-water").hide();
    })

        /********************
     * 页面按钮绑定事件
     * */
    // 排行
    $("#rank-btn").on('tap', function () {
        $("#rank-widget").show();
    })

    // 提醒
    $("#tips-btn").on('tap', function () {
        $("#message-widget").show();
    })

    //加好友
    $("#friends").on('tap', function () {
        $("#add-friend-widget").show();
    })
    //浇水
    $("#water-flower").on('tap', function () {
        $("#water-widget").show();
        $("user_message_water_time").text(myDate.getDate())
        //TODO：这里加入浇水的动态特效，翻转啊啥的
    })
    //历史
    $("#history").on('tap', function () {
        $("#history-widget").show();
    })
    //心愿
    $('#willing').on('tap', function () {
        $("#willing-widget").show();
    })

    /********************
     * 弹出框的按钮绑定事件
     * */

     // TODO:下拉出现刷新请求按钮
     //历史弹出框
    $("#message-close").on('tap', function () {
        $("#message-widget").hide();
    })

    //消息弹出框
    $("#message-close").on('tap', function () {
        $("#message-widget").hide();
    })

    //$("#message-pull").on('tap', function () {
    //    $.post(
    //        'http://1.blesstree.sinaapp.com/wechat/ajax',
    //        {
    //            'ajax_type': 3,
    //            'openid': $("#user_message_openid").text(),
    //            'load_begin': msgpull
    //
    //        },
    //        function () {
    //
    //        }
    //    )
    //    msgpull = msgpull + 5;
    //})

    //心愿弹出框
    $("#willing-close").on('tap', function () {
        $("#willing-widget").hide();
    })
    $("#willing-add").on('tap', function () {
        $('#fill-willing').show();
    })
    //填写心愿弹出框
    $("#fill-willing-close").on('tap', function(){
        $('#fill-willing').hide();
    })
    $("#fill-willing-btn").on('tap', function () {
        $('#fill-willing').hide();
        $.post('http://1.blesstree.sinaapp.com/wechat/ajax',
            {
                'ajax_type':8,
                'openid': $("#user_message_openid").text(),
                'will_con': $("#fill-area").val()
            },
            function(ret) {
                if (ret == '1') {
                    alert("提交成功！");
                    $("#willing-list").html("<li> <a style='float: left;width: 20%;font-size: 80%; text-align: center'>"+
                        $.lqcGetTimeInteval(myDate.getDate())+
                        "</a> <a style='float:left;margin-left: 20%'>"+
                        $("#fill-area").val()+
                        "</a> </li>"
                    );
                    $("#fill-willing").hide();
                } else if (ret == "2") {
                    alert("您的网络有问题，请再试一下哦～");
                } else {
                    alert("网络不太好，请再试一下哦～");
                }
            })
    })

    //祝福吐槽祝福框
    $("#history-close").on('tap', function () {
        $("#history-widget").hide()
    })

    $("#history-bless").on('tap', function () {
        $("#history-tucao-list").hide();
        $("#history-bless-list").show();
    });
    //$("#history-bless-pull").on('tap', function(){
    //    $.post('http://1.blesstree.sinaapp.com/wechat/ajax',
    //        {
    //            'ajax_type': 5,
    //            'openid': $("#user_message_openid").text(),
    //            'load_begin': blesspull
    //        },
    //        function () {
    //            alert("刷新成功～")
    //        }
    //    )
    //    blesspull = blesspull + 5; //每提交一次获取更后面的
    //})

    $("#history-tucao").on('tap', function () {
        $("#history-bless-list").hide();
        $("#history-tucao-list").show();

    })
    //$("#history-tucao-pull").on('tap', function () {
    //    $.post('http://1.blesstree.sinaapp.com/wechat/ajax',
    //        {
    //            'ajax_type': 6,
    //            'openid': $("#user_message_openid").text(),
    //            'load_begin': tucaopull
    //        },
    //        function () {
    //            alert("刷新成功～")
    //        }
    //        tucaopull = tucaopull + 5
    //    )
    //})

    //排行榜
      $("#rank-close").on('tap', function () {
          $("#rank-widget").hide();
      })
    //$("#rank-pull").on("tap", function () {
    //    $.post(
    //        'http://1.blesstree.sinaapp.com/wechat/ajax',
    //        {
    //            'ajax_type':2,
    //            'openid': $("#user_message_openid").text(),
    //            'load_begin': rankpull
    //        },
    //        function () {
    //
    //        }
    //    )
    //    rankpull = rankpull + 5
    //})

    //加好友
    $("#add-friend-widget-btn").on('tap', function () {
        $("#add-friend-widget").hide();
    })

    $("#count-enough-btn").on('tap', function () {
        $("#count-enough").hide();
    })


    /********************
     * 一些函数
     * */

    //初始化事件
     function init_main(myDate){
        $('#black-mask').show();
        $('#rule').show();

        //定时器事件,用于定时提醒浇水
        window.setInterval(function () {
            $("#time-to-water").fadeIn(1000);
            $("#time-to-water").fadeOut(1000);
        },600000);
        window.setInterval(function () {
            //定时请求消息刷新
            $.post(
            'http://1.blesstree.sinaapp.com/wechat/ajax',
            {
                'ajax_type': 3,
                'openid': $("#user_message_openid").text(),
                'load_begin': 0

            },
            function () {

            }
        )
        },180000);

    };
})
