// filepath: /Users/geomth/Downloads/NCATS/scripts/deploy.js
async function main() {
  const [deployer] = await ethers.getSigners();
  console.log("Deploying contracts with the account:", deployer.address);

  const NellCarpoolFunding = await ethers.getContractFactory("NellCarpoolFunding");
  const contract = await NellCarpoolFunding.deploy(
    "0xYourDepositAddressHere", // Replace with a valid address
    ethers.utils.parseEther("10"), // Initial Ether limit
    ethers.utils.parseEther("1000"), // Initial Token limit
    { value: ethers.utils.parseEther("100") } // Initial deposit
  );

  console.log("Contract deployed to:", contract.address);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });