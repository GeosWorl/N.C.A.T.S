const hre = require("hardhat");
const fs = require("fs");
const path = require("path");

/**
 * Deployment script for ContractAgreement smart contract
 * This script deploys the business agreement contract with the specified parties
 */
async function main() {
  console.log("=".repeat(60));
  console.log("Starting ContractAgreement Deployment");
  console.log("=".repeat(60));

  // Get the deployer account
  const [deployer] = await hre.ethers.getSigners();
  console.log("\nDeploying contracts with the account:", deployer.address);
  
  // Get account balance
  const balance = await hre.ethers.provider.getBalance(deployer.address);
  console.log("Account balance:", hre.ethers.formatEther(balance), "ETH");

  // Load addresses from environment variables or use defaults
  const borrowerAddress = process.env.BORROWER_ADDRESS || "0xAf227Cf67c13B54246B5220608fee8ee000Dbe53";
  const lenderAddress = process.env.LENDER_ADDRESS || "0xAf227Cf67c13B54246B5220608fee8ee000Dbe53";

  // Validate addresses
  if (!hre.ethers.isAddress(borrowerAddress)) {
    throw new Error("Invalid borrower address. Please provide a valid Ethereum address.");
  }
  if (!hre.ethers.isAddress(lenderAddress)) {
    throw new Error("Invalid lender address. Please provide a valid Ethereum address.");
  }

  console.log("\nContract Parameters:");
  console.log("  Borrower Address:", borrowerAddress);
  console.log("  Lender Address:", lenderAddress);
  console.log();

  // Get the contract factory
  const ContractAgreement = await hre.ethers.getContractFactory("ContractAgreement");
  
  console.log("Deploying ContractAgreement...");
  
  // Deploy the contract
  const contract = await ContractAgreement.deploy(borrowerAddress, lenderAddress);
  
  // Wait for deployment to complete
  await contract.waitForDeployment();
  
  const contractAddress = await contract.getAddress();
  
  console.log("\n" + "=".repeat(60));
  console.log("✓ Contract deployed successfully!");
  console.log("=".repeat(60));
  console.log("\nDeployment Details:");
  console.log("  Contract Address:", contractAddress);
  console.log("  Transaction Hash:", contract.deploymentTransaction().hash);
  console.log("  Block Number:", contract.deploymentTransaction().blockNumber);
  console.log("  Network:", hre.network.name);
  
  // Get contract details
  const details = await contract.getContractDetails();
  console.log("\nContract Information:");
  console.log("  Borrower:", details.borrowerAddress);
  console.log("  Lender:", details.lenderAddress);
  console.log("  Active:", details.active);
  console.log("  Loan Amount:", details.loanAmount.toString(), "USD");

  // Save deployment information
  const deploymentInfo = {
    network: hre.network.name,
    contractAddress: contractAddress,
    transactionHash: contract.deploymentTransaction().hash,
    blockNumber: contract.deploymentTransaction().blockNumber,
    deployer: deployer.address,
    borrowerAddress: borrowerAddress,
    lenderAddress: lenderAddress,
    timestamp: new Date().toISOString(),
    contractData: {
      borrower: {
        name: "Cory K Washington",
        company: "Nells Carpool and Transportation Services C-Corporation Franchise",
        role: "Owner",
        address: borrowerAddress
      },
      lender: {
        name: "Investor",
        amount: 63000000,
        currency: "USD",
        address: lenderAddress
      },
      ownership: {
        owner: "Cory K Washington (Geo)",
        ownershipPercentage: 100,
        description: "Cory K Washington (Geo) is 100% the only owner of this contract address and its companies; ownership is non-transferable."
      },
      purposes: [
        "Expand, develop, purchase new equipment and an app for Nells Carpool and Transportation Services",
        "Pay franchise fee for a nearby company (this food is to die for)",
        "Relaunch fashion brand 4-Ever-Drip in Italy"
      ],
      financialTerms: {
        amount: 6300000,
        shoeProductionTarget: 7,
        priceRange: { min: 200, max: 500 },
        material: "Raw Italian material and cotton"
      }
    }
  };

  // Create deployments directory if it doesn't exist
  const deploymentsDir = path.join(__dirname, "..", "deployments");
  if (!fs.existsSync(deploymentsDir)) {
    fs.mkdirSync(deploymentsDir, { recursive: true });
  }

  // Save deployment info to file
  const deploymentFile = path.join(
    deploymentsDir,
    `${hre.network.name}-${Date.now()}.json`
  );
  fs.writeFileSync(deploymentFile, JSON.stringify(deploymentInfo, null, 2));
  
  console.log("\n✓ Deployment info saved to:", deploymentFile);
  console.log("\n" + "=".repeat(60));
  console.log("Deployment Complete!");
  console.log("=".repeat(60));
}

// Execute the deployment
main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error("\n" + "=".repeat(60));
    console.error("Error deploying contract:");
    console.error("=".repeat(60));
    console.error(error);
    process.exit(1);
  });
