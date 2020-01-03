// JavaScript Document
$('.navbar-nav li').click(function() {
    if($(this).data('href')) {
        location.href = $(this).data('href');
    }
}); 
$('.more').click(function() {
    if($(this).data('href')) {
        location.href = $(this).data('href');
    }
});
function login() {
    $("#dengluzhuce").css("display", "block");
    $("#dengluzhuce .shuru .one").css("border-bottom", "1px solid  #e7863a").siblings('#dengluzhuce .shuru .two').css("border-bottom", "none");
};
function register() {
    $("#dengluzhuce").css("display", "block");
    $("#dengluzhuce .shuru .two").css("border-bottom", "1px solid  #e7863a").siblings('#dengluzhuce .shuru .one').css("border-bottom", "none");
};

// 验证手机号
function isPhoneNo(phone) {
    var pattern = /^1[34578]\d{9}$/;
    return pattern.test(phone);
}   
$(document).ready(function () {
 $(".close img").click(function () {
     $("#dengluzhuce").fadeOut(1000);
     $("#top").fadeOut(1);
 });

 $(".shuru .tijiao").click(function () {
             // 判断手机号码
             if ($.trim($('#phone').val()).length == 0) {
                 // str += '手机号没有输入\n';
                 $("#tip").text('请输入手机号');
                 $("#tip").show();
                 $('#phone').focus();
                 return;
             } else {
                 if (isPhoneNo($.trim($('#phone').val())) == false) {
                     // str += '手机号码不正确\n';
                     $("#tip").text('请输入正确的手机号');
                     $("#tip").show();
                     $('#phone').focus();
                     return;
                 }
             }
             if ($.trim($('#pwd').val()).length == 0) {
                 $("#tip").text('请输入密码');
                 $("#tip").show();
                 $('#pwd').focus();
                 return;
             }
             $("#tip").hide();
             $("#dengluzhuce").fadeOut(1000);
             $("#top").fadeIn(1);
             $(".nav .denglu").fadeOut(1);
             $(".nav .haibao").fadeIn(1);
         });


$(".nav .denglu").click(function () {
    $("#dengluzhuce").fadeIn(500);
});
$(".nav .denglu").mouseover(function () {
    $(".denglu p").css({"background-color": "#e7863a", "color": "rgba(0,0,0,0.8)"});
});
$(".nav .denglu").mouseleave(function () {
    $(".nav .denglu p").css({"background-color": "#e7863a", "color": "rgba(255,255,255,0.7)"});
});

$(".shuru .two").click(function () {
    $(".shuru .one").css({"border-bottom": "solid 1px rgba(255,255,255,0)", "color": "#e7863a"});
    $(".shuru .two").css({"border-bottom": "solid 1px  #e7863a", "color": "#e7863a"});
    $(".shuru form .yincang").show();
    $(".shuru form .denglu").hide();
});

$(".shuru .one").click(function () {
    $(".shuru .two").css({"border-bottom": "solid 1px rgba(255,255,255,0)", "color": "#e7863a"});
    $(".shuru .one").css({"border-bottom": "solid 1px  #e7863a", "color": "#e7863a"});
    $(".shuru form .yincang").hide();
    $(".shuru form .denglu").show();
});

});