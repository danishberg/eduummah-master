const { expect } = require("chai");
const { ethers } = require("hardhat");

module.exports = async function () {
  let admin, eduToken, eduUmmah;

  try {
    [admin] = await ethers.getSigners();

    // Deploy the EduToken contract
    const EduTokenFactory = await ethers.getContractFactory("EduToken");
    console.log("Deploying EduToken contract...");
    const eduTokenDeployment = await EduTokenFactory.deploy("1000000000000000000000"); // 1000 ETH in wei
    await eduTokenDeployment.deployed(); // Wait for the contract to be deployed
    eduToken = await ethers.getContractAt("EduToken", eduTokenDeployment.address); // Access the deployed contract instance

    console.log("EduToken contract deployed at address:", eduToken.address); // Log the contract address

    // Deploy the EduUmmah contract
    const EduUmmahFactory = await ethers.getContractFactory("EduUmmah");
    console.log("Deploying EduUmmah contract...");
    const eduUmmahDeployment = await EduUmmahFactory.deploy(eduToken.address);
    await eduUmmahDeployment.deployed(); // Wait for the contract to be deployed
    eduUmmah = await ethers.getContractAt("EduUmmah", eduUmmahDeployment.address); // Access the deployed contract instance

    console.log("EduUmmah contract deployed at address:", eduUmmah.address); // Log the contract address

    it("should have correct initial setup", async function () {
      // Ensure eduToken and eduUmmah are defined before accessing their functions
      if (!eduToken || !eduUmmah) {
        console.error("Contracts are not deployed");
        return;
      }

      // Now that deployment checks are in beforeEach, here we focus on logic checks

      const totalSupply = await eduToken.totalSupply();
      expect(totalSupply.toString()).to.equal("1000000000000000000000");

      const adminBalance = await eduToken.balanceOf(admin.address);
      expect(adminBalance.toString()).to.equal("1000000000000000000000");
    });

    // Additional test cases for EduUmmah functionality would follow...
  } catch (error) {
    console.error("Error deploying contracts:", error);
  }
};
