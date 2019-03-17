EosApi = require('eosjs-api');

let options = {
    httpEndpoint: 'http://bp.cryptolions.io:8888',
};

let eos = EosApi(options);


function calculate_vote_weight(time, staked_tokens) {
    let seconds_2000 = new Date('2000-01-01');
    let time_since_2000 = (time - seconds_2000.getTime()) / 1000 ;
    let weight = (time_since_2000 / 604800) / 52;
    return (staked_tokens) * 2**weight;
}

function calculate_decay(staked_tokens, last_vote_weight) {
    return last_vote_weight / calculate_vote_weight(Date.now(), staked_tokens) * 100
}


async function getData() {
    try {
        let result = await eos.getProducers({'json': true});
        let producers = result.rows;

        for (let p of producers) {
            console.log("===============================================================");
            let owner_info  = await eos.getAccount(p.owner);
            let staked_tokens = owner_info.voter_info.staked;

            console.log("owner:", p.owner);
            console.log("url:", p.url);
            console.log("staked tokens:", staked_tokens);
            console.log("total votes:", p.total_votes);
            console.log("is active:", p.is_active === 1 ? "true" : "false");
            if (p.is_active === 1) {
                console.log("vote weight:", owner_info.voter_info.last_vote_weight);
                console.log("decay:", calculate_decay(staked_tokens, owner_info.voter_info.last_vote_weight));
            }

        }
    } catch (e) {
        console.log(e)
    }
}


getData();