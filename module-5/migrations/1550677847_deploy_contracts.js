let Hello = artifacts.require("./Hello.sol");

module.exports = function(deployer, _network, _accounts) {

    deployer.deploy(Hello, "hello");
}