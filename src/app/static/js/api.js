var app=angular.module('myapp',[]);

app.controller('apiController',function($scope,$http){
$scope.callLogin=function(userid){
	$http.post('/login',userid).success(function(data){alert("success1");}).error(function(){alert("error");})};
}
);

