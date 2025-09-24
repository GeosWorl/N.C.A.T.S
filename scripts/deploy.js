async function main() {
  const [deployer] = await ethers.getSigners();
  console.log("Deploying contracts with the account:", deployer.address);

  // Define the depositor address
  const depositorAddress = "0xEE9115A1096630056da826494448B833f138DECd"; // Depositor address

  // Validate the depositor address
  if (!ethers.utils.isAddress(depositorAddress)) {
    throw new Error("Invalid depositor address. Please provide a valid Ethereum address.");
  }

  // Deploy the contract
  const NellCarpoolFunding = await ethers.getContractFactory("NellCarpoolFunding");
  const contract = await NellCarpoolFunding.deploy(
    depositorAddress, // Pass the depositor address to the constructor
    ethers.utils.parseEther("10"), // Initial Ether limit
    ethers.utils.parseEther("100000"), // Initial Token limit
    { value: ethers.utils.parseEther("100") } // Initial deposit
  );

  console.log("Contract deployed to:", contract.address);
  console.log("Depositor address:", depositorAddress);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error("Error deploying contract:", error);
    process.exit(1);
  });