# N.C.A.T.S - Nell's Carpool and Transportation Services

Transportation Company with Smart Contract Integration

## Overview

This repository contains:
1. **Smart Contract Infrastructure**: Ethereum-based business agreement between borrower and lender parties
2. **Flask Web Application**: User-facing web interface with authentication, applications, and smart contract integration

## Quick Start

### Smart Contract Development

**New to smart contracts?** See the [Quick Start Guide](QUICKSTART.md) for a 5-minute setup!

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md)

#### Installation

```bash
npm install
```

#### Configure Environment

```bash
cp .env.example .env
# Edit .env with your configuration
```

#### Deploy Contract

```bash
# Local development
npm run deploy:localhost

# Sepolia testnet
npm run deploy:sepolia

# Ethereum mainnet
npm run deploy:mainnet
```

### Flask Web Application

For the web application setup and usage, see [FLASK_README.md](FLASK_README.md)

#### Quick Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with Flask configuration

# Initialize database
python3 init_db.py

# Run the application
python app.py
```

The web application provides:
- User authentication (registration, login, password reset)
- User profiles with application history
- Application submission with file upload
- Integration with the Ethereum smart contract
- Security features (CSRF protection, rate limiting, input validation)

## Documentation

- [Quick Start Guide](QUICKSTART.md) - 5-minute smart contract setup guide
- [Deployment Guide](DEPLOYMENT.md) - Complete smart contract deployment instructions
- [Contract Documentation](contracts/ContractAgreement.sol) - Smart contract details
- [Flask Application Guide](FLASK_README.md) - Web application setup and usage

## Project Structure

```
.
├── contracts/                  # Smart contract files
│   └── ContractAgreement.sol  # Main business agreement contract
├── scripts/                    # Deployment scripts
├── test/                       # Smart contract tests
├── app.py                      # Flask web application
├── models.py                   # Database models
├── templates/                  # HTML templates
├── static/                     # CSS and static files
├── requirements.txt            # Python dependencies
├── package.json                # Node.js dependencies
└── hardhat.config.js          # Hardhat configuration
```

## License

Boost Software License - Version 1.0
