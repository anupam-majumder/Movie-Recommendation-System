var app=angular.module('myapp',[]);

app.controller('apiController',function($scope,$http){
$scope.seenButton = 'gray';
$scope.predButton = 'gray';
$scope.rateButton = 'gray';
$scope.hide = true;
$scope.hideNav = false;
$scope.hidePredicted = false;
$scope.hideSeen = false;
$scope.hideRate = false;
$scope.userid = "";
$scope.active = true;
$scope.callLogin=function(userid){
    $scope.seenButton = 'skyblue';
    $scope.predButton = 'gray';
    $scope.rateButton = 'gray';
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
    $scope.seenButton = 'gray';
    $scope.predButton = 'skyblue';
    $scope.rateButton = 'gray';
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
    $scope.seenButton = 'gray';
    $scope.predButton = 'gray';
    $scope.rateButton = 'skyblue';
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

$scope.callPutRating=function(){
    let i, ratings=[];
    for(i=0; i<$scope.rate.length;i++){
        let temp={};
        temp["userid"] = $scope.userid;
        temp["id"]=$scope.rate[i].id;
        temp["rating"]=document.getElementById($scope.rate[i].id).value;
        ratings.push(temp);        
    }
    console.log(ratings);
	$http.post('http://localhost:12394/setRating',ratings).then(function readData(response){
		console.log(response.data);
        $scope.hideRate = false;
        $scope.hide = false;
        $scope.hideSeen = true;
        $scope.hideNav = true;
        $scope.hidePredicted = false;
        
	}
)};   
    
$scope.myButton = 'default';
 $scope.changeBgColor = function() {
     $scope.myButton = "clicked";
};
}
);
