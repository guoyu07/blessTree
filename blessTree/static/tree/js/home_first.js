/**
 * Created by albert on 15-12-7.
 */
/**
 * Created by albert on 15-11-29.
 */

$(function () {

    alert("success")

    init_main();
    
    /********************
     * 按钮绑定事件
     * */

    //排行按钮
    $('#rank').on('tap', function () {
        $.post(
            'http://1.blesstree.sinaapp.com/wechat/ajax',
            {
                openid: 'openid',
                nickname: 'nickname'
            },
            function () {
                alert("成功ajax推送到服务器")
            }
        )
    })

    //心愿按钮
    

    //下一步按钮
    $('#rule-next').on('tap', function () {
        $('#rule').hide();
    })

    /********************
     * 一些函数
     * */

    //初始化事件
     function init_main(){
        $('#black-mask').show();
    };
})
