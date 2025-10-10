const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("ContractAgreement", function () {
  let contractAgreement;
  let owner;
  let borrower;
  let lender;
  let addr1;

  beforeEach(async function () {
    // Get test accounts
    [owner, borrower, lender, addr1] = await ethers.getSigners();

    // Deploy the contract
    const ContractAgreement = await ethers.getContractFactory("ContractAgreement");
    contractAgreement = await ContractAgreement.deploy(borrower.address, lender.address);
    await contractAgreement.waitForDeployment();
  });

  describe("Deployment", function () {
    it("Should set the correct contract owner", async function () {
      expect(await contractAgreement.contractOwner()).to.equal(owner.address);
    });

    it("Should set the correct borrower address", async function () {
      const borrowerInfo = await contractAgreement.borrower();
      expect(borrowerInfo.walletAddress).to.equal(borrower.address);
    });

    it("Should set the correct lender address", async function () {
      const lenderInfo = await contractAgreement.lender();
      expect(lenderInfo.walletAddress).to.equal(lender.address);
    });

    it("Should initialize with inactive status", async function () {
      expect(await contractAgreement.isActive()).to.equal(false);
    });

    it("Should set correct borrower details", async function () {
      const borrowerInfo = await contractAgreement.borrower();
      expect(borrowerInfo.name).to.equal("Cory K Washington");
      expect(borrowerInfo.company).to.equal("Nells Carpool and Transportation Services C-Corporation Franchise");
      expect(borrowerInfo.role).to.equal("Owner");
    });

    it("Should set correct lender details", async function () {
      const lenderInfo = await contractAgreement.lender();
      expect(lenderInfo.name).to.equal("Investor");
      expect(lenderInfo.amount).to.equal(63000000);
      expect(lenderInfo.currency).to.equal("USD");
    });

    it("Should set correct ownership details", async function () {
      const ownershipInfo = await contractAgreement.ownership();
      expect(ownershipInfo.owner).to.equal("Cory K Washington (Geo)");
      expect(ownershipInfo.ownershipPercentage).to.equal(100);
    });

    it("Should set correct financial terms", async function () {
      const financialTerms = await contractAgreement.financialTerms();
      expect(financialTerms.amount).to.equal(6300000);
      expect(financialTerms.shoeProductionTarget).to.equal(7);
      expect(financialTerms.priceMin).to.equal(200);
      expect(financialTerms.priceMax).to.equal(500);
      expect(financialTerms.material).to.equal("Raw Italian material and cotton");
    });

    it("Should have the correct number of purposes", async function () {
      const purposesCount = await contractAgreement.getPurposesCount();
      expect(purposesCount).to.equal(3);
    });

    it("Should fail deployment with zero borrower address", async function () {
      const ContractAgreement = await ethers.getContractFactory("ContractAgreement");
      await expect(
        ContractAgreement.deploy(ethers.ZeroAddress, lender.address)
      ).to.be.revertedWith("Invalid borrower address");
    });

    it("Should fail deployment with zero lender address", async function () {
      const ContractAgreement = await ethers.getContractFactory("ContractAgreement");
      await expect(
        ContractAgreement.deploy(borrower.address, ethers.ZeroAddress)
      ).to.be.revertedWith("Invalid lender address");
    });
  });

  describe("Contract Activation", function () {
    it("Should allow owner to activate contract", async function () {
      await contractAgreement.connect(owner).activateContract();
      expect(await contractAgreement.isActive()).to.equal(true);
    });

    it("Should not allow non-owner to activate contract", async function () {
      await expect(
        contractAgreement.connect(addr1).activateContract()
      ).to.be.revertedWith("Only contract owner can call this function");
    });

    it("Should not allow activating an already active contract", async function () {
      await contractAgreement.connect(owner).activateContract();
      await expect(
        contractAgreement.connect(owner).activateContract()
      ).to.be.revertedWith("Contract is already active");
    });

    it("Should emit ContractActivated event", async function () {
      await expect(contractAgreement.connect(owner).activateContract())
        .to.emit(contractAgreement, "ContractActivated");
    });
  });

  describe("Accept Terms", function () {
    it("Should allow borrower to accept terms", async function () {
      await expect(contractAgreement.connect(borrower).acceptTerms())
        .to.emit(contractAgreement, "ContractTermsAccepted")
        .withArgs(borrower.address, await ethers.provider.getBlock("latest").then(b => b.timestamp + 1));
    });

    it("Should allow lender to accept terms", async function () {
      await expect(contractAgreement.connect(lender).acceptTerms())
        .to.emit(contractAgreement, "ContractTermsAccepted")
        .withArgs(lender.address, await ethers.provider.getBlock("latest").then(b => b.timestamp + 1));
    });

    it("Should not allow non-party to accept terms", async function () {
      await expect(
        contractAgreement.connect(addr1).acceptTerms()
      ).to.be.revertedWith("Only parties can call this function");
    });
  });

  describe("View Functions", function () {
    it("Should return purposes correctly", async function () {
      const purpose0 = await contractAgreement.getPurpose(0);
      const purpose1 = await contractAgreement.getPurpose(1);
      const purpose2 = await contractAgreement.getPurpose(2);

      expect(purpose0).to.equal("Expand, develop, purchase new equipment and an app for Nells Carpool and Transportation Services");
      expect(purpose1).to.equal("Pay franchise fee for a nearby company (this food is to die for)");
      expect(purpose2).to.equal("Relaunch fashion brand 4-Ever-Drip in Italy");
    });

    it("Should revert when accessing purpose with invalid index", async function () {
      await expect(
        contractAgreement.getPurpose(10)
      ).to.be.revertedWith("Index out of bounds");
    });

    it("Should return contract details correctly", async function () {
      const details = await contractAgreement.getContractDetails();
      expect(details.borrowerAddress).to.equal(borrower.address);
      expect(details.lenderAddress).to.equal(lender.address);
      expect(details.active).to.equal(false);
      expect(details.loanAmount).to.equal(63000000);
    });

    it("Should return correct contract details after activation", async function () {
      await contractAgreement.connect(owner).activateContract();
      const details = await contractAgreement.getContractDetails();
      expect(details.active).to.equal(true);
    });
  });

  describe("Events", function () {
    it("Should emit ContractDeployed on deployment", async function () {
      // Deploy a new instance to test the event
      const ContractAgreement = await ethers.getContractFactory("ContractAgreement");
      await expect(ContractAgreement.deploy(borrower.address, lender.address))
        .to.emit(await ContractAgreement.deploy(borrower.address, lender.address), "ContractDeployed");
    });
  });
});
