var app=angular.module('myapp',[]);
app.controller('apiController',function($scope,$http){
$scope.callLogin=function(userid){
	user = userid;
	$http.post('/login',userid).then(function readData(response){
		console.log(response.data.userid);
        console.log(response.data.recommends);
        $scope.mv=response.data.recommends;
        console.log($scope.mv[0].url)
        $scope.myarray = [{"url":"https://images-na.ssl-images-amazon.com/images/M/MV5BNDE0NTQ1NjQzM15BMl5BanBnXkFtZTYwNDI4MDU5..jpg","movie":"movie1"},{"url":"https://images-na.ssl-images-amazon.com/images/M/MV5BNDE0NTQ1NjQzM15BMl5BanBnXkFtZTYwNDI4MDU5..jpg","movie":"movie2"},{"url":"https://images-na.ssl-images-amazon.com/images/M/MV5BNDE0NTQ1NjQzM15BMl5BanBnXkFtZTYwNDI4MDU5..jpg","movie":"movie3"}]
	}
)};
}
);
