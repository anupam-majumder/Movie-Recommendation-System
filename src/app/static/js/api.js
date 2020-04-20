var app=angular.module('myapp',[]);
var user;
app.controller('apiController',function($window,$scope,$http,$location){
$scope.callLogin=function(userid){
	user = userid;
	$http.post('/login',userid).then(function readData(response){
		console.log(response.data.userid);
		$window.location.href = '/welcome';

	}
)};
}
);
