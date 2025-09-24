# Code Citations

## License: unknown
https://github.com/figment-networks/figment-docs/tree/9b0fd210c1b9f320146032e7b4596c73be1748b2/network-documentation/celo/tutorial/deploying-smart-contracts-on-celo-with-truffle.md

```
0;

contract Migrations {
    address public owner = msg.sender;
    uint public last_completed_migration;

    modifier restricted() {
        require(msg.sender == owner, "This function is restricted to the contract's owner");
        _;
    }

    function setCompleted(uint completed) public
```


## License: unknown
https://github.com/jwalin12/UniswapRenter/tree/bfba9d2a03794c7d9b4295eb869a90fadfc5afec/scripts/deploy.js

```
.log("Contract deployed to:", contract.address);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1)
```

