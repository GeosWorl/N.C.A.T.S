{
  "contract": {
    "name": "NellsCarpoolFunding",
    "version": "1.0.0",
    "description": "A funding contract for Nell's Carpool And Transportation Services with advanced security features including active honeypot, time-lock until ~2100, emergency stop, and restricted ownership.",
    "license": "MIT",
    "solidityVersion": "^0.8.0",
    "sourceCode": "// SPDX-License-Identifier: MIT\npragma solidity ^0.8.0;\n\n/// @title NellCarpoolFunding - Funding contract for Nell's Carpool And Transportation Services\n/// @notice Accepts Ether, allows owner-controlled withdrawals, and can safely send ERC20 tokens\n/// @dev Implements advanced security with active honeypot, time-lock, emergency stop, and ownership controls\n/// @dev Deployer (representing Cory K Washington) is the initial owner with restricted transfer\n\nimport \"@openzeppelin/contracts/security/ReentrancyGuard.sol\";\nimport \"@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol\";\nimport \"@openzeppelin/contracts/utils/Address.sol\";\n\ncontract NellCarpoolFunding is ReentrancyGuard {\n    // Full contract code as shown above\n}",
    "keyParameters": {
      "timeLockDelay": {
        "value": "2430000000 seconds",
        "description": "Approximates a delay until the year 2100 (~77 years from 2023) for critical actions like ownership transfer and large withdrawals.",
        "effectiveUntil": "Approximately January 1, 2100 (based on deployment in 2023)"
      },
      "initialOwner": {
        "value": "Deployer address (msg.sender at deployment)",
        "description": "Represents Cory K Washington as the initial owner with restricted transfer capabilities."
      },
      "initialDeposit": {
        "value": "10000 ETH",
        "description": "Contract must be initialized with at least 10000 ETH, forwarded to depositAddress during deployment."
      },
      "trapCooldown": {
        "value": "1 hour",
        "description": "Cooldown period imposed on addresses triggering the honeypot via invalid calls."
      }
    },
    "securityFeatures": {
      "activeHoneypot": {
        "description": "Logs suspicious activity and imposes a temporary cooldown on malicious callers via fallback function.",
        "events": ["SuspiciousActivity", "Trapped"]
      },
      "timeLock": {
        "description": "Delays critical actions (ownership transfer, large withdrawals) until approximately year 2100.",
        "events": ["ActionQueued", "ActionExecuted", "OwnershipTransferQueued"]
      },
      "emergencyStop": {
        "description": "Halts all operations including withdrawals in case of emergency.",
        "events": ["EmergencyStopActivated", "EmergencyStopDeactivated"]
      },
      "reentrancyGuard": {
        "description": "Prevents reentrancy attacks using OpenZeppelin's ReentrancyGuard."
      },
      "withdrawalLimits": {
        "description": "Enforces daily limits on Ether and token withdrawals to mitigate damage from compromised keys.",
        "events": ["WithdrawalLimitsUpdated"]
      },
      "safeERC20": {
        "description": "Uses OpenZeppelin's SafeERC20 for secure token handling."
      }
    },
    "deploymentNotes": {
      "requirements": {
        "dependencies": "OpenZeppelin contracts (^4.0.0 or compatible version)",
        "initialFunds": "At least 10000 ETH to be sent during deployment"
      },
      "recommendations": {
        "testnetTesting": "Test on Sepolia or similar testnet for time-lock, honeypot, and emergency stop functionality.",
        "monitoring": "Set up off-chain monitoring for SuspiciousActivity, Trapped, and ActionQueued events.",
        "audit": "Professional audit recommended due to long time-lock and complex security mechanisms."
      }
    },
    "risks": {
      "timeLockDuration": "Extremely long time-lock (~77 years) effectively makes critical actions like ownership transfer or large withdrawals impossible until 2100, risking permanent lockout if needs change.",
      "ownership": "Even with time-locked transfer, owner key security is critical. Loss or compromise could lock funds or allow unauthorized access after 2100.",
      "honeypotImpact": "Cooldown trap may temporarily affect legitimate users who accidentally trigger fallback; monitor Trapped events to mitigate."
    }
  }
}