// EduToken.test.js

const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("EduToken", function () {
  let owner, recipient, spender;
  let token;
  const initialSupply = "1000000000000000000000"; // 1000 tokens considering 18 decimals.

  beforeEach(async function () {
    [owner, recipient, spender] = await ethers.getSigners();
    const EduToken = await ethers.getContractFactory("EduToken");
    token = await EduToken.deploy(initialSupply);
  });

  describe("Deployment", function () {
    it("should assign the total supply of tokens to the owner", async function () {
      expect(await token.totalSupply()).to.equal(initialSupply);
      expect(await token.balanceOf(owner.address)).to.equal(initialSupply);
    });
  });

  describe("Transfer functionality", function () {
    it("should transfer tokens between accounts", async function () {
      await token.transfer(recipient.address, "100000000000000000000"); // 100 tokens
      expect(await token.balanceOf(owner.address)).to.equal("900000000000000000000"); // 900 tokens
      expect(await token.balanceOf(recipient.address)).to.equal("100000000000000000000"); // 100 tokens
    });
  });

  describe("Approval and Allowance", function () {
    it("should approve and check the allowance", async function () {
      await token.approve(spender.address, "50000000000000000000"); // 50 tokens
      expect(await token.allowance(owner.address, spender.address)).to.equal("50000000000000000000");
    });
  });

  describe("Rejection of Invalid Transactions", function () {
    it("should not allow transferring more tokens than the account holds", async function () {
      await expect(token.transfer(recipient.address, "2000000000000000000000")).to.be.reverted;
    });
  });
});
