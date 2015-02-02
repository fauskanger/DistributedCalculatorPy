var app = angular.module('distCalcApp', ['ngRoute']);

app.controller('DistCalcController', ['$scope', function ($scope) {
    $scope.operations = [
        { sign: "+", name: "add" },
        { sign: "-", name: "subtract" },
        { sign: "*", name: "multiply" },
        { sign: "/", name: "divide" },
        { sign: "^", name: "power" }
    ];
    
    $scope.operand1 = 2;
    $scope.operand2 = 3;
}]);