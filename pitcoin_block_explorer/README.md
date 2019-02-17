# pitcoin_block_explorer

> A Vue.js project

## Build Setup

``` bash
# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev
```

If you are building the whole thing on the raspberry, remember to edit config/index.js.

All you have to do is modify the port value inside the dev block:

```
 dev: {
    assetsSubDirectory: 'static',
    assetsPublicPath: '/',
    proxyTable: {},

    host: '10.86.1.3',
    port: 8080, 
    autoOpenBrowser: false,
    errorOverlay: true,
    notifyOnErrors: true,
    poll: false,

```

