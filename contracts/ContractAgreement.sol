// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title ContractAgreement
 * @dev Smart contract representing the business agreement between borrower and lender
 * @notice This contract is deployed at address 0x721ED067e04dC811c94c9A0C45b6160De799E2C0
 */
contract ContractAgreement {
    
    // Contract metadata
    address public constant CONTRACT_ADDRESS = 0x721ED067e04dC811c94c9A0C45b6160De799E2C0;
    
    // Parties
    struct Borrower {
        string name;
        string company;
        string role;
        string borrowerAccount;
        address walletAddress;
    }
    
    struct Lender {
        string name;
        uint256 amount;
        string currency;
        string apiKey;
        address walletAddress;
    }
    
    // Ownership
    struct Ownership {
        string owner;
        uint256 ownershipPercentage;
        string description;
    }
    
    // Financial terms
    struct FinancialTerms {
        uint256 amount;
        uint256 shoeProductionTarget;
        uint256 priceMin;
        uint256 priceMax;
        string material;
    }
    
    // State variables
    Borrower public borrower;
    Lender public lender;
    Ownership public ownership;
    FinancialTerms public financialTerms;
    
    string[] public purposes;
    address public contractOwner;
    bool public isActive;
    
    // Events
    event ContractDeployed(address indexed deployer, uint256 timestamp);
    event ContractActivated(uint256 timestamp);
    event ContractTermsAccepted(address indexed party, uint256 timestamp);
    
    // Modifiers
    modifier onlyOwner() {
        require(msg.sender == contractOwner, "Only contract owner can call this function");
        _;
    }
    
    modifier onlyParties() {
        require(
            msg.sender == borrower.walletAddress || msg.sender == lender.walletAddress,
            "Only parties can call this function"
        );
        _;
    }
    
    /**
     * @dev Constructor to initialize the contract with the agreement details
     * @param _borrowerAddress Borrower's wallet address
     * @param _lenderAddress Lender's wallet address
     */
    constructor(address _borrowerAddress, address _lenderAddress) {
        require(_borrowerAddress != address(0), "Invalid borrower address");
        require(_lenderAddress != address(0), "Invalid lender address");
        
        contractOwner = msg.sender;
        isActive = false;
        
        // Initialize Borrower
        borrower = Borrower({
            name: "Cory K Washington",
            company: "Nells Carpool and Transportation Services C-Corporation Franchise",
            role: "Owner",
            borrowerAccount: "Your Deposit Account",
            walletAddress: _borrowerAddress
        });
        
        // Initialize Lender
        lender = Lender({
            name: "Investor",
            amount: 63000000,
            currency: "USD",
            apiKey: "Your API Key",
            walletAddress: _lenderAddress
        });
        
        // Initialize Ownership
        ownership = Ownership({
            owner: "Cory K Washington (Geo)",
            ownershipPercentage: 100,
            description: "Cory K Washington (Geo) is 100% the only owner of this contract address and its companies; ownership is non-transferable."
        });
        
        // Initialize Financial Terms
        financialTerms = FinancialTerms({
            amount: 6300000,
            shoeProductionTarget: 7,
            priceMin: 200,
            priceMax: 500,
            material: "Raw Italian material and cotton"
        });
        
        // Add purposes
        purposes.push("Expand, develop, purchase new equipment and an app for Nells Carpool and Transportation Services");
        purposes.push("Pay franchise fee for a nearby company (this food is to die for)");
        purposes.push("Relaunch fashion brand 4-Ever-Drip in Italy");
        
        emit ContractDeployed(msg.sender, block.timestamp);
    }
    
    /**
     * @dev Activate the contract
     */
    function activateContract() external onlyOwner {
        require(!isActive, "Contract is already active");
        isActive = true;
        emit ContractActivated(block.timestamp);
    }
    
    /**
     * @dev Accept contract terms by a party
     */
    function acceptTerms() external onlyParties {
        emit ContractTermsAccepted(msg.sender, block.timestamp);
    }
    
    /**
     * @dev Get the number of purposes
     * @return The count of purposes
     */
    function getPurposesCount() external view returns (uint256) {
        return purposes.length;
    }
    
    /**
     * @dev Get a specific purpose by index
     * @param index The index of the purpose
     * @return The purpose string
     */
    function getPurpose(uint256 index) external view returns (string memory) {
        require(index < purposes.length, "Index out of bounds");
        return purposes[index];
    }
    
    /**
     * @dev Get contract details
     * @return Borrower and Lender wallet addresses, active status
     */
    function getContractDetails() external view returns (
        address borrowerAddress,
        address lenderAddress,
        bool active,
        uint256 loanAmount
    ) {
        return (
            borrower.walletAddress,
            lender.walletAddress,
            isActive,
            lender.amount
        );
    }
}
