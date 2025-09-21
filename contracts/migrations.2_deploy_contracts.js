// filepath: /Users/geomth/Downloads/NCATS/migrations/2_deploy_contracts.js
const NellCarpoolFunding = artifacts.require("NellCarpoolFunding");

module.exports = function (deployer) {
  const depositAddress = "0xYourDepositAddressHere"; // Replace with a valid address
  const initialEtherLimit = web3.utils.toWei("10", "ether"); // Example: 10 ETH
  const initialTokenLimit = web3.utils.toWei("1000", "ether"); // Example: 1000 tokens

  deployer.deploy(NellCarpoolFunding, depositAddress, initialEtherLimit, initialTokenLimit, {
    value: web3.utils.toWei("100", "ether"), // Initial deposit of 100 ETH
  });
};