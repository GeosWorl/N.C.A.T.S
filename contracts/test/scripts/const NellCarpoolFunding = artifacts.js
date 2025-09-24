const NellCarpoolFunding = artifacts.require("NellCarpoolFunding");

module.exports = function (deployer) {
  const initialEtherLimit = web3.utils.toWei("10", "ether"); // Example: 10 ETH
  const initialTokenLimit = web3.utils.toWei("1000", "ether"); // Example: 1000 tokens

  deployer.deploy(NellCarpoolFunding, "0xEE9115A1096630056da826494448B833f138DECd", initialEtherLimit, initialTokenLimit, {
    value: web3.utils.toWei("100", "ether"), // Initial deposit of 100 ETH
  });
};