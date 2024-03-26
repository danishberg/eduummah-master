// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract EduUmmah {
    IERC20 public token;

    struct Learner {
        bool isRegistered;
        uint256 progress;
    }

    address public admin;
    mapping(address => Learner) public learners;

    event LearnerRegistered(address learner);
    event ProgressUpdated(address learner, uint256 newProgress, uint256 reward);

    constructor(IERC20 _tokenAddress) {
        admin = msg.sender;
        token = _tokenAddress;
    }

    function registerLearner() public {
        require(!learners[msg.sender].isRegistered, "Learner is already registered.");
        learners[msg.sender] = Learner(true, 0);
        emit LearnerRegistered(msg.sender);
    }

    function updateProgress(uint256 _newProgress) public {
        require(learners[msg.sender].isRegistered, "Learner is not registered.");
        require(_newProgress > learners[msg.sender].progress, "New progress must be greater than current progress.");

        uint256 reward = _newProgress - learners[msg.sender].progress;
        learners[msg.sender].progress = _newProgress;

        require(token.transfer(msg.sender, reward), "Failed to transfer tokens.");

        emit ProgressUpdated(msg.sender, _newProgress, reward);
    }

    function getLearnerDetails(address learner) public view returns (bool isRegistered, uint256 progress) {
        Learner memory l = learners[learner];
        return (l.isRegistered, l.progress);
    }
}
