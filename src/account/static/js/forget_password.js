(function () {
    'use strict';
    angular.module('reFound', []).controller('FoundPassword', [
        '$scope', function ($scope) {

            $scope.passwordvalid = function (password) {
                if (password) {
                    if (password.password1 && password.password2) {
                        return !(password.password1 == password.password2);
                    } else {
                        return true;
                    }
                } else {
                    return true;
                }
            };

            $scope.confirm = function (password) {
                if (password.password1 != password.password2) {
                    $scope.message2 = true;
                } else {
                    $scope.message2 = false;
                }
            };

            $scope.explain = function () {
                $scope.message = true;
            };
            $scope.explainDisappear = function () {
                $scope.message = false;
            }

        }])
})();