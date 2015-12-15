/**
 * Created by albert on 15-12-4.
 */

/*定制jquery属性*/
(function ($) {
    //定义全局变量

    //祝福——吐槽的摘要长度
    $.LQC_DETAIL_TENGTH = 40;
    //每次加载的祝福/吐槽的数目
    $.LQC_DETAIL_LOAD_COUNT = 7;
    //每次加载的朋友数目
    $.LQC_FRIEND_LOAD_COUNT = 7;

    //初始化ajax
    $.ajaxSetup({
        type:'POST'
    });

    //常用的函数
    
    //获取GET参数
    $.lqcGetUrlParam = function (name) {
        var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
        var r = window.location.search.substr(1).match(reg);
        if (r != null) return unescape(r[2]);
        return null;
    }

    //
})(jQuery)