var app=angular.module('myapp',[]);
app.controller('apiController',function($scope,$http){
$scope.callLogin=function(userid){
	user = userid;
	$http.post('http://localhost:12394/login',userid).then(function readData(response){
		console.log(response.data.userid);
        console.log(response.data.recommends);
        $scope.mv=response.data.recommends;
	}
)};
}
);
