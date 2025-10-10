# N.C.A.T.S - Nell's Carpool and Transportation Services

Transportation Company with Smart Contract Integration

## Overview

This repository contains the smart contract infrastructure for N.C.A.T.S (Nell's Carpool and Transportation Services), implementing a blockchain-based business agreement between borrower and lender parties.

## Quick Start

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md)

### Installation

```bash
npm install
```

### Configure Environment

```bash
cp .env.example .env
# Edit .env with your configuration
```

### Deploy Contract

```bash
# Local development
npm run deploy:localhost

# Sepolia testnet
npm run deploy:sepolia

# Ethereum mainnet
npm run deploy:mainnet
```

## Documentation

- [Deployment Guide](DEPLOYMENT.md) - Complete deployment instructions
- [Contract Documentation](contracts/ContractAgreement.sol) - Smart contract details

## License

Boost Software License - Version 1.0
