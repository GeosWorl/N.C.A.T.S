// filepath: /Users/geomth/Downloads/NCATS/test/NellCarpoolFunding.test.js
const NellCarpoolFunding = artifacts.require("NellCarpoolFunding");

contract("NellCarpoolFunding", (accounts) => {
  const [owner, user] = accounts;

  it("should deploy the contract with the correct owner", async () => {
    const contract = await NellCarpoolFunding.deployed();
    const contractOwner = await contract.owner();
    assert.equal(contractOwner, owner, "Owner is not set correctly");
  });

  it("should allow deposits", async () => {
    const contract = await NellCarpoolFunding.deployed();
    await contract.deposit({ from: user, value: web3.utils.toWei("1", "ether") });
    // Add assertions to verify deposit behavior
  });

  // Add more tests for withdrawals, emergency stop, etc.
});