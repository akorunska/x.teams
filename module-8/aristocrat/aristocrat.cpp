#include <eosiolib/eosio.hpp>
#include <math.h>

using namespace eosio;

class [[eosio::contract]] aristocrat : public contract {
    public:
    using contract::contract;

    [[eosio::action]]
    void drink( std::string guess, std::string randomness) {
        int seed = 0;
        int sum = 0;
        std::string drink = "";

        for(int i = 0; i < randomness.size(); i++) {
            sum += randomness[i];
        }

        if (guess != "red" && guess != "white") {
            printf("Those drinks are not known. Please choose red or white.");
        }

        if (sum % 2 == 0)
            drink = "red";
        else
            drink = "white";

        if (drink == guess) {
            printf("Yes, indeed, that is what I want to drink this evening! ");
            printf("You win, my dear sir / lady.");
        } else {
            printf("Oh, what a poor taste. I shall drink champagne instead.");
            printf("You lose,  my dear sir / lady.");
        }
    }
};

EOSIO_DISPATCH( aristocrat, (drink))
