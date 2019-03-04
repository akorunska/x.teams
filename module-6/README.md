# Post-Satoshi Era: module 6

The aim of this week is to deal with smart contracts security.

(o>o)

## Izi

Complete all levels of Ethernaut game - https://ethernaut.zeppelin.solutions


Num | Level name           | Level instance address                     |
----| ---------------------|--------------------------------------------|
0  | Hello Ethernaut      |                                            |
1  | Fallback             | 0x7e21ec06d6b2a24e79c6a88903d033354086c9d6 |
2  | Fallout              | 0x4d2d4d90b1c03ea5d0db73bb9432cfc9c3eb0973 |
3  | Coin Flip            | 0xeb89b380011d19b2ea8bc3cbd4585924bc35055a |
4  | Telephone            | 0xfdf1bc2fee23c9e1d6d9b2504bc96c1097846228 |
5  | Token                | 0x2fb23b96adb7ef2a95bd2cef5093a6dd5763be98 |
6  | Delegation           | 0x06ed6c5fa6738e87e460b5bce8202c44e6a50ba3 |
7  | Force                | 0x1137c1a1eeb22e507b21822827142ed4fd67d711 |
8  | Vault                | 0xc6c1481341e6961d59d3f45a85fea388b550fa8d |
9  | King                 | 0x0a0374a1d74bf12750c265beee89c840bfcd6639 |
10 | Re-entrancy          | 0xfb99093c6035e2728f86dc5482217c5d006c7ca2 |
11 | Elevator             | 0x33382b9f8eab070385fa1a3d6e3ebfa4f731eb46 |
12 | Privacy              | 0xbf6650cf40fa7050a940779172398aa101e43617 |
13 | Gatekeeper One       | 0x178b711efd00c21bd04862ed0f31d6421c0930bd |
14 | Gatekeeper Two       | 0x4c56d0dc144acbf435876d199fba7979574eac41 |
15 | NaughtCoin           | 0x87fc69300086ccc615132c5e506746007b22f2be |
16 | Preservation         | 0x4d1ab5a9cd797705d4552f9d67421558110d6c19 |
17 | Locked               | 0x81390c89fd009ce7f9b55328731ee822284fe2c2 |
18 | Recovery             | 0x609c147b54f59fe606e2b0a37d5700e8ea4a7318 |
19 | Magic Number         | 0x62ff0d10597e42844a7f54b422bb2718171a9748 |
20 | Alien Codex          | 0x108c93901887e7b0acd5bb3b60dd5e76a04d2f77 |
21 | Denial               | 0x601c7951500f83ed1da63ab031b435d4e551683a |
22 | Shop                 | 0x412faaa1ced833f56fa09e01391576d474b4805d |


Address used to complete all levels is `0xa3E1aB154F40d984E56fF07d1EEa46a50BD8ee36`.


## Hard

1. Enter own_game/ and install dependensies:
    ```
    npm install
    
    ```

2. Start local network.
    ```
    ganache-cli --deterministic
    
    ```

3. Copy one of the private keys and import it to the Metamask. (Remember to switch to localhost net)

4. Compile and deploy the contracts.
   ```
   npx truffle compile
   npm run deploy:contracts
   ```
5. Start the server and enjoy playing!
    ```
    npm start
    ```
