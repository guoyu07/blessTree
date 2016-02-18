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

    //格式化时间处理
    $.lqcGetTimeInteval = function (time) {
        var myDate = new Date();
        inteval = (myDate-time)/1000
        if(inteval>3600*24){
            return (inteval/(3600*24)).toString()+'天前'
        }else if(inteval>3600){
            return (inteval/3600).toString()+'小时前'
        }else if(inteval>60){
            return (inteval/60).toString()+'分钟前'
        }else{
            return '刚刚'
        }
    }

    //生成随机数 范围：0-n
    $.lqcRandGenerator = function (n) {
        parseInt((n-1)*Math.random())
    }

    $.preventDefault = function(e) {
            e = e || window.event;
            e.preventDefault && e.preventDefault();
            e.returnValue = false;
        }

    $.stopPropagation = function(e){
        e = e || window.event;
        e.stopPropagation && e.stopPropagation();
        e.cancelBubble = false;
    }

    $.innerScroll = function(e){
        // 阻止冒泡到document
        // document上已经preventDefault
        stopPropagation(e);

        var delta = e.wheelDelta || e.detail || 0;
        var box = $(this).get(0);

        if($(box).height() + box.scrollTop >= box.scrollHeight){
            if(delta < 0) {
                preventDefault(e);
                return false;
            }
        }
        if(box.scrollTop === 0){
            if(delta > 0) {
                preventDefault(e);
                return false;
            }
        }
        // 会阻止原生滚动
        // return false;
    }

    $.disableScroll = function(){
        $(document).on('mousewheel', preventDefault);
        $(document).on('touchmove', preventDefault);
    };

    $.enableScroll = function(){
        $(document).off('mousewheel', preventDefault);
        $(document).off('touchmove', preventDefault);
    };

    //
})(jQuery)