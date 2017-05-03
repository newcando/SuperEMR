function getCookie(name){
        var arr,reg=new RegExp("(^| )"+name+"=([^;]*)(;|$)");
        if(arr=document.cookie.match(reg))
            return unescape(arr[2]);
        else
            return null;
    }
var rongcloudToken = getCookie("rongcloudToken");//$.cookie("rongcloudToken");
rongcloudToken = rongcloudToken.substring(1,rongcloudToken.length - 1);
console.log(rongcloudToken);
var demo = angular.module("demo", ["RongWebIMWidget"]);
demo.controller("main", ["$scope", "WebIMWidget", "$http", function($scope, WebIMWidget, $http) {
    $scope.targetType = 1; //1：私聊 更多会话类型查看http://www.rongcloud.cn/docs/api/js/global.html#ConversationType
    $scope.targetId = 'test';
    //注意实际应用中 appkey 、 token 使用自己从融云服务器注册的。
    WebIMWidget.init({
        appkey: "pwe86ga5ep576",
        token: rongcloudToken,
        displayConversationList: true,
        style:{
            left:3,
            bottom:3,
            width:430
        },
        onSuccess: function(id) {
            $scope.user = id;
            //document.title = '用户：' + id;
            console.log('连接成功：' + id);
        },
        onError: function(error) {
            console.log('连接失败：' + error);
        }
    });
    //接收到消息时
    WebIMWidget.onReceivedMessage = function(message) {
      //message 收到的消息
      console.log('收到的消息：' + message);
    };

    WebIMWidget.setUserInfoProvider(function(targetId, obj) {
        obj.onSuccess({
            name: "用户：" + targetId
        });
    });
    WebIMWidget.setGroupInfoProvider(function(targetId, obj){
        obj.onSuccess({
            name:'群组：' + targetId
        });
    });
    $scope.setconversation = function() {
        var a = $scope.targetId;
        var id = $("#patientIDHidden").val();
        var name = $("#patientUsernameHidden").val();
        if (!!$scope.targetId) {
            WebIMWidget.setConversation(Number($scope.targetType), id, "用户：" + name);
            WebIMWidget.show();
        }
    };
    $scope.show = function() {
        WebIMWidget.show();
    };
    $scope.hidden = function() {
        WebIMWidget.hidden();
    };
    WebIMWidget.show();
    // 示例：获取 userinfo.json 中数据，根据 targetId 获取对应用户信息
    // WebIMWidget.setUserInfoProvider(function(targetId,obj){
    //     $http({
    //       url:"/userinfo.json"
    //     }).success(function(rep){
    //       var user;
    //       rep.userlist.forEach(function(item){
    //         if(item.id==targetId){
    //           user=item;
    //         }
    //       })
    //       if(user){
    //         obj.onSuccess({id:user.id,name:user.name,portraitUri:user.portraitUri});
    //       }else{
    //         obj.onSuccess({id:targetId,name:"用户："+targetId});
    //       }
    //     })
    // });

    // 示例：获取 online.json 中数据，根据传入用户 id 数组获取对应在线状态
    // WebIMWidget.setOnlineStatusProvider(function(arr, obj) {
    //     $http({
    //         url: "/online.json"
    //     }).success(function(rep) {
    //         obj.onSuccess(rep.data);
    //     })
    // });
}]);