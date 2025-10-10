# Quick Start Guide

This is a streamlined guide to get you deploying the ContractAgreement smart contract quickly.

## Prerequisites Checklist

- [ ] Node.js v16 or later installed
- [ ] An Ethereum wallet with funds
- [ ] RPC URL (Infura, Alchemy, or similar)
- [ ] Private key from your wallet

## 5-Minute Setup

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` file:
```bash
# Required for deployment
PRIVATE_KEY=your_private_key_without_0x_prefix

# Required for testnet/mainnet
SEPOLIA_RPC_URL=https://sepolia.infura.io/v3/YOUR_PROJECT_ID
MAINNET_RPC_URL=https://mainnet.infura.io/v3/YOUR_PROJECT_ID

# Optional
ETHERSCAN_API_KEY=your_etherscan_api_key
BORROWER_ADDRESS=0xAf227Cf67c13B54246B5220608fee8ee000Dbe53
LENDER_ADDRESS=0xAf227Cf67c13B54246B5220608fee8ee000Dbe53
```

### 3. Verify Setup

```bash
npm run verify-setup
```

### 4. Compile Contracts

```bash
npm run compile
```

### 5. Deploy

**Local Testing:**
```bash
# Terminal 1: Start local node
npm run node

# Terminal 2: Deploy to local network
npm run deploy:localhost
```

**Testnet (Recommended for testing):**
```bash
npm run deploy:sepolia
```

**Mainnet (Production):**
```bash
npm run deploy:mainnet
```

## Post-Deployment

After successful deployment, you'll receive:
- Contract address
- Transaction hash
- Deployment record in `deployments/` directory

## Contract Details

The deployed contract stores:
- Borrower: Cory K Washington (Nells Carpool and Transportation Services)
- Lender: Investor with $63,000,000 funding
- Business purposes and financial terms
- 100% non-transferable ownership

## Getting Help

- Full documentation: [DEPLOYMENT.md](DEPLOYMENT.md)
- View contract: `contracts/ContractAgreement.sol`
- Troubleshooting: See DEPLOYMENT.md

## Important Security Notes

⚠️ **Never commit your `.env` file to git**
⚠️ **Test on testnet before mainnet deployment**
⚠️ **Keep your private key secure**

## Verify Everything is Ready

```bash
npm run verify-setup
```

If all checks pass, you're ready to deploy! 🚀
