# N.C.A.T.S - Nell's Carpool and Transportation Services

Transportation Company with Smart Contract Integration

## Overview

This repository contains the smart contract infrastructure for N.C.A.T.S (Nell's Carpool and Transportation Services), implementing a blockchain-based business agreement between borrower and lender parties.

## Features

- **Smart Contract Infrastructure**: Blockchain-based business agreements
- **Web Application**: Flask-based web interface with user authentication
- **User Authorization**: Secure login, registration, and session management
- **Protected Routes**: Access control for authenticated users
- **API Endpoints**: RESTful API for integration

## Quick Start

**New to this?** See the [Quick Start Guide](QUICKSTART.md) for a 5-minute setup!

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md)

For Flask web application setup, see [FLASK_README.md](FLASK_README.md)

### Smart Contract Setup

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

### Flask Web Application Setup

#### Installation

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### Running the Application

```bash
python run.py
```

The application will be available at `http://localhost:5000`

#### Features

- User registration and login
- Secure password hashing with Werkzeug
- Session-based authentication
- Protected dashboard for authenticated users
- Comprehensive test suite

For detailed Flask documentation, see [FLASK_README.md](FLASK_README.md)

## Documentation

- [Quick Start Guide](QUICKSTART.md) - 5-minute setup guide
- [Deployment Guide](DEPLOYMENT.md) - Complete deployment instructions
- [Flask Application Guide](FLASK_README.md) - Web application setup and usage
- [Contract Documentation](contracts/ContractAgreement.sol) - Smart contract details

## License

Boost Software License - Version 1.0
