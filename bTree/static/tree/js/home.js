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


    //心愿按钮
    


    /********************
     * 一些函数
     * */
    
    //初始化事件
     function init_main(){

        //TODO：刚刚进入提示浇水，注意数据库查询不到water_time的时候在渲染模板的时候传来一个0值
        var water_time = $("#user_message_water_time").text();
        var myDate = new Date()
        if((myDate.getTime()-water_time)/(1000*60)>10){
            $("#time-water-btn").show()
        }
        //定时器事件,用于定时提醒浇水
        window.setInterval(function () {
            $("#time-water-btn").fadeIn(1000);
            $("#time-water-btn").fadeOut(1000);
        },600000);
    };
})
