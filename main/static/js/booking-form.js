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
    // To avoid fractional issues, all values are converted to pennies before final tally
    let totalCost = 0;
    let isPlayer = true;
    let isCatering = false;
    let formIsValid = false;

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

    const playerCostValue = parseFloat(document.getElementById('player_cost_value').value) * 100;
    const monsterCostValue = parseFloat(document.getElementById('monster_cost_value').value) * 100;
    const playerCateringCostValue = parseFloat(document.getElementById('player_catering_cost_value').value) * 100;
    const monsterCateringCostValue = parseFloat(document.getElementById('monster_catering_cost_value').value) * 100;

    const totalCostDisplay = document.getElementById('total_cost');

    totalCost = playerCostValue;

    characterNameInput.required = true;
    characterFactionInput.required = true;

    const initPayPalButton = () => {
        if (formIsValid) {
            paypal.Buttons({
                style: {
                    shape: 'rect',
                    color: 'gold',
                    layout: 'vertical',
                    label: 'paypal',
                },

                createOrder: function (data, actions) {
                    const eventName = document.getElementById('event-title').innerText

                    return actions.order.create({
                        purchase_units: [{
                            "description": `Event Booking for '${eventName}'`,
                            "amount": {
                                "currency_code": "GBP",
                                "value": totalCost / 100
                            }
                        }]
                    });
                },

                onApprove: function (data, actions) {
                    return actions.order.capture().then(function (orderData) {

                        // Full available details
                        console.log('Capture result', orderData, JSON.stringify(orderData, null, 2));

                        // Show a success message within this page, e.g.
                        const element = document.getElementById('paypal-button-container');
                        element.innerHTML = '';
                        element.innerHTML = '<h3>Thank you for your payment!</h3>';

                        bookingForm.submit()
                    });
                },

                onError: function (err) {
                    console.log(err);
                }
            }).render('#paypal-button-container');
        }
    }

    const validateForm = () => {
        [...bookingForm.elements].forEach(field => {
            if (field.classList.contains('is-danger')) {
                field.classList.remove('is-danger');
                const validationErrorMessage = field.parentElement.querySelector('.fetch-validation-error')
                if (validationErrorMessage) {
                    validationErrorMessage.remove()
                }
            }
        })

        fetch('/validate-booking/', {body: new FormData(bookingForm), method: 'POST'})
            .then(response => {
                const buttonContainer = document.getElementById('paypal-button-container');
                buttonContainer.innerHTML = '';

                if (!response.ok) {
                    formIsValid = false;
                    response.json().then(json => {
                        Object.keys(json).forEach(key => {
                            const field_errors = json[key]
                            field_errors.forEach(field_error => {
                                if (field_error.code !== 'required') {
                                    const field = bookingForm[key];
                                    field.classList.add('is-danger')
                                    const ErrorNode = document.createElement('div');
                                    ErrorNode.classList.add('help', 'is-danger', 'fetch-validation-error')
                                    ErrorNode.innerText = field_error.message;
                                    field.parentElement.appendChild(ErrorNode)
                                }
                            })
                        })
                    })
                } else {
                    formIsValid = bookingForm.checkValidity();
                }

                if (formIsValid) {
                    if (totalCost > 0) {
                        initPayPalButton()
                    } else {
                        buttonContainer.innerHTML = '<input class="button is-link is-large is-fullwidth" type="submit" value="Submit">';
                    }
                } else {
                    buttonContainer.innerHTML = '<div class="block has-background-light p-6"><p>Please ensure you have filled in all required fields in order to finish booking</p></div>'
                }
            })
            .catch(error => {
                formIsValid = false;
                console.error('ERROR - The following error occurred:', error)
                console.error('Please contact Jackals Faction staff with more details')
            })
    }

    const calculateCosts = () => {
        totalCost = isPlayer ? playerCostValue : monsterCostValue;

        if (isCatering) {
            totalCost += isPlayer ? playerCateringCostValue : monsterCateringCostValue;
        }

        totalCostDisplay.innerText = (totalCost / 100).toFixed(2)

        validateForm()
    }

    const initForm = () => {
        const selector = document.getElementById('id_player_type')

        switch (selector.value) {
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

        calculateCosts()
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

        calculateCosts()
    })

    initForm()
})
