var demo = angular.module("demo", ["RongWebIMWidget"]);

demo.controller("main", ["$scope", "WebIMWidget", function($scope, WebIMWidget) {

    $scope.targetType = 1; //1：私聊 更多会话类型查看http://www.rongcloud.cn/docs/api/js/global.html#ConversationType
    $scope.targetId = 'aa';

    WebIMWidget.init({
        appkey: "bmdehs6pdw0ss",
        token: "T0EAr02cSZ816H/fm/POi8vVz5jKjrGTX+4hbq436lxI+TXY9FPwG5cKBWb4Qi4YAoL8QbzPDDo=",
        style:{
            left:3,
            bottom:3,
            width:430
        },
        displayConversationList: true,
        onSuccess: function(id) {
            $scope.user = id;
            document.title = '用户：' + id;
            console.log('连接成功：' + id);
        },
        onError: function(error) {
            console.log("连接失败：" + error);
        }
    });

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
        if (!!$scope.targetId) {
            WebIMWidget.setConversation(Number($scope.targetType), $scope.targetId, "用户：" + $scope.targetId);
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
}]);