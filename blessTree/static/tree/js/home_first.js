/**
 * Created by albert on 15-12-7.
 */
/**
 * Created by albert on 15-11-29.
 */

$(function () {

    init_main();
    
    /********************
     * 按钮绑定事件
     * */

    //排行按钮
    $('#rank').on('tap', function () {
        alert("you click it")
        $.post('http://1.blesstree.sinaapp.com/wechat/ajax',
            {'openid':'openid','nickname':'nickname'},
            function(ret) {
                if(ret=='1'){
                alert("提交成功！");
            }
            else if(ret=="2"){
               alert("请输入标题和内容！");
            }
            else{
               alert("系统错误！");
            }
    })

    //心愿按钮
    

    //下一步按钮
    $('#rule-next').on('tap', function () {
        $('#rule').hide();
        $('#black-mask').hide();
    })

    /********************
     * 一些函数
     * */

    //初始化事件
     function init_main(){
        $('#black-mask').show();
        $('#rule').show();
    };
})
