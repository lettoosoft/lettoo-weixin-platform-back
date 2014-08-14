(function () {
    'use strict';
    angular.module('reFound', []).controller('FoundPassword', [
        '$scope', function ($scope) {

            $scope.passwordvalid = function (password) {
                if ($scope.danger2) {
                    return true;
                } else {
                    if (password) {
                        if (password.password1 && password.password2) {
                            return !(password.password1 == password.password2);
                        } else {
                            return true;
                        }
                    } else {
                        return true;
                    }
                }
            };
            $scope.confirm = function (password) {
                if (password.password1 != password.password2) {
                    $scope.danger1 = true;
                } else {
                    $scope.danger1 = false;
                }
            };
            $scope.explain = function () {
                $scope.info = true;
            };
            $scope.explainDisappear = function () {
                var re = /[^a-zA-Z0-9_]+/g;
                if (re.test($scope.password.password1)) {
                    $scope.danger2 = true;
                } else {
                    $scope.danger2 = false;
                }
                $scope.info = false;
            }

        }])
})();
