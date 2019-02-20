const Hello = artifacts.require("Hello");


contract("Hello", function(accounts) {
    let contract;

    beforeEach(async () => {
        contract = await Hello.new("hello")
    });

    it("says hello", async () => {
        const msg = await contract.message();

        assert.equal("hello", msg);
    });
});