# N.C.A.T.S Smart Contract Deployment

Transportation Company with Smart Contract Integration

## Overview

This repository contains the smart contract deployment infrastructure for the N.C.A.T.S (Nell's Carpool and Transportation Services) business agreement. The contract represents a formal business agreement between a borrower (Cory K Washington) and a lender for funding various business initiatives.

## Contract Details

The `ContractAgreement` smart contract stores and manages:

- **Borrower Information**: Cory K Washington representing Nells Carpool and Transportation Services C-Corporation Franchise
- **Lender Information**: Investor with $63,000,000 USD funding commitment
- **Ownership**: 100% ownership by Cory K Washington (Geo), non-transferable
- **Business Purposes**:
  - Expand, develop, purchase new equipment and an app for Nells Carpool and Transportation Services
  - Pay franchise fee for a nearby company
  - Relaunch fashion brand 4-Ever-Drip in Italy
- **Financial Terms**: $6,300,000 with shoe production milestones ($200-$500 price range)

## Prerequisites

- Node.js (v16 or later)
- npm or yarn package manager
- An Ethereum wallet with funds for deployment
- RPC URL for the target network (Infura, Alchemy, etc.)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/GeosWorl/N.C.A.T.S.git
cd N.C.A.T.S
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables:
```bash
cp .env.example .env
```

4. Edit `.env` file with your configuration:
```
PRIVATE_KEY=your_private_key_without_0x_prefix
SEPOLIA_RPC_URL=https://sepolia.infura.io/v3/YOUR_PROJECT_ID
MAINNET_RPC_URL=https://mainnet.infura.io/v3/YOUR_PROJECT_ID
ETHERSCAN_API_KEY=your_etherscan_api_key
BORROWER_ADDRESS=0xAf227Cf67c13B54246B5220608fee8ee000Dbe53
LENDER_ADDRESS=0xAf227Cf67c13B54246B5220608fee8ee000Dbe53
```

⚠️ **Security Warning**: Never commit your `.env` file or expose your private keys!

## Compilation

Compile the smart contracts:

```bash
npm run compile
```

This will compile all contracts in the `contracts/` directory and generate artifacts in the `artifacts/` directory.

## Deployment

### Local Development Network

1. Start a local Hardhat node:
```bash
npm run node
```

2. In a new terminal, deploy to localhost:
```bash
npm run deploy:localhost
```

### Sepolia Testnet

Deploy to Sepolia testnet (recommended for testing):

```bash
npm run deploy:sepolia
```

### Ethereum Mainnet

⚠️ **Warning**: Mainnet deployment costs real ETH. Ensure you have tested thoroughly on testnets first.

```bash
npm run deploy:mainnet
```

## Deployment Output

After successful deployment, the script will:

1. Display deployment details including:
   - Contract address
   - Transaction hash
   - Block number
   - Network name
   - Borrower and Lender addresses
   - Loan amount

2. Save deployment information to `deployments/` directory with timestamp:
   - Network details
   - Contract address
   - All contract parameters
   - Timestamp

Example output:
```
============================================================
✓ Contract deployed successfully!
============================================================

Deployment Details:
  Contract Address: 0x1234567890123456789012345678901234567890
  Transaction Hash: 0xabcdef...
  Block Number: 12345678
  Network: sepolia

Contract Information:
  Borrower: 0xAf227Cf67c13B54246B5220608fee8ee000Dbe53
  Lender: 0xAf227Cf67c13B54246B5220608fee8ee000Dbe53
  Active: false
  Loan Amount: 63000000 USD
```

## Contract Functions

### Read Functions
- `borrower()`: Get borrower details
- `lender()`: Get lender details
- `ownership()`: Get ownership information
- `financialTerms()`: Get financial terms
- `getContractDetails()`: Get summary of contract details
- `getPurposesCount()`: Get number of purposes
- `getPurpose(index)`: Get specific purpose by index
- `isActive()`: Check if contract is active

### Write Functions (Restricted)
- `activateContract()`: Activate the contract (owner only)
- `acceptTerms()`: Accept contract terms (parties only)

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `PRIVATE_KEY` | Private key of deploying account (without 0x) | Yes |
| `SEPOLIA_RPC_URL` | RPC URL for Sepolia testnet | For testnet |
| `MAINNET_RPC_URL` | RPC URL for Ethereum mainnet | For mainnet |
| `ETHERSCAN_API_KEY` | API key for contract verification | Optional |
| `BORROWER_ADDRESS` | Ethereum address of the borrower | Optional* |
| `LENDER_ADDRESS` | Ethereum address of the lender | Optional* |

*If not provided, defaults to `0xAf227Cf67c13B54246B5220608fee8ee000Dbe53`

## Testing

Run contract tests (if available):

```bash
npm test
```

## Contract Verification

After deployment, verify your contract on Etherscan:

```bash
npx hardhat verify --network sepolia <CONTRACT_ADDRESS> <BORROWER_ADDRESS> <LENDER_ADDRESS>
```

Replace `<CONTRACT_ADDRESS>`, `<BORROWER_ADDRESS>`, and `<LENDER_ADDRESS>` with actual values.

## Security Considerations

1. **Private Keys**: Never commit private keys to version control
2. **Environment Variables**: Always use `.env` for sensitive data
3. **Testing**: Thoroughly test on testnets before mainnet deployment
4. **Audit**: Consider a professional security audit for mainnet deployments
5. **Access Control**: The contract has owner and party restrictions for sensitive functions

## Project Structure

```
N.C.A.T.S/
├── contracts/
│   ├── ContractAgreement.sol    # Main business agreement contract
│   └── Migrations.sol            # Truffle migrations contract
├── scripts/
│   ├── deployContract.js         # Deployment script with full logging
│   └── deploy.js                 # Legacy deployment script
├── deployments/                  # Deployment records (generated)
├── .env.example                  # Example environment variables
├── .gitignore                    # Git ignore file
├── hardhat.config.js             # Hardhat configuration
├── package.json                  # Node.js dependencies
└── README.md                     # This file
```

## Troubleshooting

### "Insufficient funds" error
Ensure your deployer account has enough ETH to cover gas fees.

### "Invalid private key" error
Check that your `PRIVATE_KEY` in `.env` is correct and doesn't include the "0x" prefix.

### "Network not configured" error
Verify your RPC URLs are correct in `.env` and accessible.

### Compilation errors
Run `npm install` to ensure all dependencies are installed.

## Support

For issues or questions, please open an issue in the GitHub repository.

## License

This project is licensed under the Boost Software License - Version 1.0. See the [LICENSE](LICENSE) file for details.

## Authors

- Cory K Washington (Geo) - Owner and Creator
- N.C.A.T.S Development Team

## Acknowledgments

- OpenZeppelin for secure smart contract libraries
- Hardhat development environment
- The Ethereum community
