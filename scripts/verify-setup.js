#!/usr/bin/env node

/**
 * Pre-deployment verification script
 * Checks that all necessary files and configurations are in place
 */

const fs = require('fs');
const path = require('path');

console.log('='.repeat(60));
console.log('Contract Deployment Pre-flight Check');
console.log('='.repeat(60));
console.log();

let allChecksPass = true;

// Check 1: Required files exist
console.log('📋 Checking required files...');
const requiredFiles = [
  'contracts/ContractAgreement.sol',
  'scripts/deployContract.js',
  'hardhat.config.js',
  'package.json',
  '.env.example',
  'DEPLOYMENT.md'
];

requiredFiles.forEach(file => {
  const filePath = path.join(__dirname, '..', file);
  if (fs.existsSync(filePath)) {
    console.log(`  ✓ ${file}`);
  } else {
    console.log(`  ✗ ${file} - MISSING`);
    allChecksPass = false;
  }
});
console.log();

// Check 2: .env file exists
console.log('🔐 Checking environment configuration...');
const envPath = path.join(__dirname, '..', '.env');
if (fs.existsSync(envPath)) {
  console.log('  ✓ .env file exists');
  
  // Check for required variables
  const envContent = fs.readFileSync(envPath, 'utf8');
  const requiredVars = ['PRIVATE_KEY'];
  const optionalVars = ['SEPOLIA_RPC_URL', 'MAINNET_RPC_URL', 'ETHERSCAN_API_KEY'];
  
  requiredVars.forEach(varName => {
    if (envContent.includes(`${varName}=`) && !envContent.includes(`${varName}=your_`)) {
      console.log(`  ✓ ${varName} is configured`);
    } else {
      console.log(`  ⚠ ${varName} needs to be set`);
    }
  });
  
  optionalVars.forEach(varName => {
    if (envContent.includes(`${varName}=`) && !envContent.includes(`${varName}=your_`) && !envContent.includes(`${varName}=https://`)) {
      console.log(`  ℹ ${varName} is configured`);
    } else {
      console.log(`  ℹ ${varName} (optional, not configured)`);
    }
  });
} else {
  console.log('  ⚠ .env file not found');
  console.log('  ℹ Run: cp .env.example .env');
  console.log('  ℹ Then edit .env with your configuration');
}
console.log();

// Check 3: Node modules installed
console.log('📦 Checking dependencies...');
const nodeModulesPath = path.join(__dirname, '..', 'node_modules');
if (fs.existsSync(nodeModulesPath)) {
  console.log('  ✓ node_modules directory exists');
  
  // Check for key packages
  const keyPackages = ['hardhat', 'dotenv', '@openzeppelin/contracts'];
  keyPackages.forEach(pkg => {
    const pkgPath = path.join(nodeModulesPath, pkg);
    if (fs.existsSync(pkgPath)) {
      console.log(`  ✓ ${pkg}`);
    } else {
      console.log(`  ✗ ${pkg} - MISSING`);
      allChecksPass = false;
    }
  });
} else {
  console.log('  ✗ node_modules not found');
  console.log('  ℹ Run: npm install');
  allChecksPass = false;
}
console.log();

// Check 4: Contract structure
console.log('📜 Checking contract structure...');
const contractPath = path.join(__dirname, '..', 'contracts', 'ContractAgreement.sol');
if (fs.existsSync(contractPath)) {
  const contractContent = fs.readFileSync(contractPath, 'utf8');
  
  // Check for key components
  const checks = [
    { pattern: /pragma solidity/, name: 'Solidity version pragma' },
    { pattern: /contract ContractAgreement/, name: 'Contract declaration' },
    { pattern: /struct Borrower/, name: 'Borrower struct' },
    { pattern: /struct Lender/, name: 'Lender struct' },
    { pattern: /constructor/, name: 'Constructor' },
    { pattern: /function activateContract/, name: 'Activate function' },
    { pattern: /function acceptTerms/, name: 'Accept terms function' }
  ];
  
  checks.forEach(check => {
    if (check.pattern.test(contractContent)) {
      console.log(`  ✓ ${check.name}`);
    } else {
      console.log(`  ✗ ${check.name} - MISSING`);
      allChecksPass = false;
    }
  });
}
console.log();

// Check 5: Deployment script structure
console.log('🚀 Checking deployment script...');
const deployScriptPath = path.join(__dirname, '..', 'scripts', 'deployContract.js');
if (fs.existsSync(deployScriptPath)) {
  const scriptContent = fs.readFileSync(deployScriptPath, 'utf8');
  
  const checks = [
    { pattern: /require\("hardhat"\)/, name: 'Hardhat import' },
    { pattern: /ethers\.getSigners/, name: 'Signer retrieval' },
    { pattern: /ContractAgreement\.deploy/, name: 'Contract deployment' },
    { pattern: /waitForDeployment/, name: 'Deployment wait' },
    { pattern: /getContractDetails/, name: 'Contract details retrieval' }
  ];
  
  checks.forEach(check => {
    if (check.pattern.test(scriptContent)) {
      console.log(`  ✓ ${check.name}`);
    } else {
      console.log(`  ✗ ${check.name} - MISSING`);
      allChecksPass = false;
    }
  });
}
console.log();

// Summary
console.log('='.repeat(60));
if (allChecksPass) {
  console.log('✅ All checks passed! Ready for deployment.');
  console.log();
  console.log('Next steps:');
  console.log('  1. Ensure .env is configured with your private key');
  console.log('  2. Compile: npm run compile');
  console.log('  3. Deploy: npm run deploy:localhost (or deploy:sepolia)');
} else {
  console.log('⚠️  Some checks failed. Please review the issues above.');
  console.log();
  console.log('Common fixes:');
  console.log('  - Run: npm install');
  console.log('  - Run: cp .env.example .env');
  console.log('  - Edit .env with your configuration');
}
console.log('='.repeat(60));

process.exit(allChecksPass ? 0 : 1);
