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
    init_main();
    
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
                //'openid': $("#user_message_openid").text(),
                //'nickname': $("user_message_nickname").text(),
                'openid': 'test',
                'nickname': 'lqczzz',
                'tree_name': tree_name
            },
            function(ret) {
                if (ret == '1') {
                    alert("提交成功！");
                } else if (ret == "2") {
                    alert("请输入标题和内容！");
                } else {
                    alert("系统错误！");
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

    //心愿按钮


    /********************
     * 一些函数
     * */

    //初始化事件
     function init_main(){
        $('#black-mask').show();
        $('#rule').show();
    };
})
