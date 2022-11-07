const PLAYER = 'PL'
const MONSTER = 'MN'

const show = (element) => {
    if (Array.isArray(element)) {
        element.forEach(elm => {show(elm)})
    } else {
        element.classList.remove('is-hidden')
    }
}

const hide = (element) => {
        if (Array.isArray(element)) {
        element.forEach(elm => {hide(elm)})
    } else {
        element.classList.add('is-hidden')
    }
}

document.addEventListener('DOMContentLoaded', () => {
    let totalCost = 0;
    let isPlayer = true;
    let isCatering = false;

    const bookingForm = document.getElementById('booking_form')
    const characterDetails = document.getElementById('character_details')
    const characterNameInput = document.getElementById('id_character_name')
    const characterFactionInput = document.getElementById('id_character_faction')
    const playerCost = document.getElementById('player_cost')
    const monsterCost = document.getElementById('monster_cost')
    const playerCateringCost = document.getElementById('player_catering_cost')
    const monsterCateringCost = document.getElementById('monster_catering_cost')

    const characterElementArray = [characterDetails, playerCost, playerCateringCost]
    const monsterElementArray = [monsterCost, monsterCateringCost]

    const playerCostValue = parseFloat(document.getElementById('player_cost_value').value);
    const monsterCostValue = parseFloat(document.getElementById('monster_cost_value').value);
    const playerCateringCostValue = parseFloat(document.getElementById('player_catering_cost_value').value);
    const monsterCateringCostValue = parseFloat(document.getElementById('monster_catering_cost_value').value);

    const totalCostDisplay = document.getElementById('total_cost');

    totalCost = playerCostValue;

    characterNameInput.required = true;
    characterFactionInput.required = true;

    const initPayPalButton = () => {
        paypal.Buttons({
            style: {
                shape: 'rect',
                color: 'gold',
                layout: 'vertical',
                label: 'paypal',
            },

            createOrder: function(data, actions) {
                return actions.order.create({
                    purchase_units: [{
                        "description": `Event Booking for ${bookingForm.email.value}`,
                        "amount":{
                            "currency_code":"GBP",
                            "value": totalCost
                        }
                    }]
                });
            },

            onApprove: function(data, actions) {
                return actions.order.capture().then(function(orderData) {

                    // Full available details
                    console.log('Capture result', orderData, JSON.stringify(orderData, null, 2));

                    // Show a success message within this page, e.g.
                    const element = document.getElementById('paypal-button-container');
                    element.innerHTML = '';
                    element.innerHTML = '<h3>Thank you for your payment!</h3>';

                    // Or go to another URL:  actions.redirect('thank_you.html');
                    bookingForm.submit()
                });
            },

            onError: function(err) {
                console.log(err);
            }
        }).render('#paypal-button-container');
    }

    bookingForm.addEventListener('change', (evt) => {
        if (evt.target.id === 'id_player_type') {
            switch (evt.target.value) {
                case PLAYER:
                    isPlayer = true;
                    show(characterElementArray);
                    hide(monsterElementArray);
                    characterNameInput.required = true;
                    characterFactionInput.required = true;
                    break;
                case MONSTER:
                    isPlayer = false;
                    hide(characterElementArray)
                    show(monsterElementArray)
                    characterNameInput.required = false;
                    characterFactionInput.required = false;
                    break;
            }
        }

        if (evt.target.id === 'id_is_catering') {
            isCatering = !!evt.target.checked;
        }

        totalCost = isPlayer ? playerCostValue : monsterCostValue;

        if (isCatering) {
            totalCost += isPlayer ? playerCateringCostValue : monsterCateringCostValue;
        }

        totalCostDisplay.innerText = totalCost.toFixed(2)

        const element = document.getElementById('paypal-button-container');
        element.innerHTML = '';

        if (totalCost > 0) {
            initPayPalButton()
        } else {
            element.innerHTML = '<input class="button is-link is-large is-fullwidth" type="submit" value="Submit">';
        }
    })

    initPayPalButton();
})
