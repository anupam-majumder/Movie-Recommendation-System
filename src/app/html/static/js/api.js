var app=angular.module('myapp',[]);

app.controller('apiController',function($scope,$http){
$scope.hide = true;
$scope.hideNav = false;
$scope.hidePredicted = false;
$scope.hideSeen = false;
$scope.hideRate = false;
$scope.userid = ""
$scope.callLogin=function(userid){
	user = userid;
	$http.post('http://localhost:12394/getSeen',userid).then(function readData(response){
		console.log(response.data.userid);
        console.log(response.data.recommends);
        $scope.mv=response.data.recommends;
        $scope.hide = false;
        $scope.hideSeen = true;
        $scope.hideNav = true;
        $scope.hidePredicted = false;
        $scope.hideRate = false;
        $scope.userid = userid;
	}
)};
     
$scope.callPredicted=function(userid){
	user = userid;
	$http.post('http://localhost:12394/getRecommendations',$scope.userid).then(function readData(response){
		console.log(response.data.userid);
        console.log(response.data.recommends);
        $scope.pre=response.data.recommends;
        $scope.hide = false;
        $scope.hideSeen = false;
        $scope.hideNav = true;
        $scope.hidePredicted = true;
        $scope.hideRate = false;
	}
)};
    
$scope.callRating=function(){
	$http.post('http://localhost:12394/getRating',$scope.userid).then(function readData(response){
		console.log(response.data.userid);
        console.log(response.data.recommends);
        $scope.rate=response.data.recommends;
        console.log($scope.rate);
        $scope.hideRate = true;
        $scope.hide = false;
        $scope.hideSeen = false;
        $scope.hideNav = true;
        $scope.hidePredicted = false;
        
	}
)};

}
);
