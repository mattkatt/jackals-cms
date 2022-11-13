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
    const bookingForm = document.getElementById('booking_form');
    const characterDetails = document.getElementById('character_details');
    const characterNameInput = document.getElementById('id_character_name');
    const characterFactionInput = document.getElementById('id_character_faction');
    const playerCost = document.getElementById('player_cost');
    const monsterCost = document.getElementById('monster_cost');
    const playerCateringCost = document.getElementById('player_catering_cost');
    const monsterCateringCost = document.getElementById('monster_catering_cost');

    const characterElementArray = [characterDetails, playerCost, playerCateringCost];
    const monsterElementArray = [monsterCost, monsterCateringCost];

    // To avoid fractional issues, all values are converted to pennies before final tally

    const playerCostValue = parseFloat(document.getElementById('player_cost_value').value) * 100;
    const monsterCostValue = parseFloat(document.getElementById('monster_cost_value').value) * 100;
    const playerCateringCostValue = parseFloat(document.getElementById('player_catering_cost_value').value) * 100;
    const monsterCateringCostValue = parseFloat(document.getElementById('monster_catering_cost_value').value) * 100;

    const totalCostDisplay = document.getElementById('total_cost');

    let isPlayer = document.getElementById('id_player_type').value === 'PL';
    let isCatering = document.getElementById('id_is_catering').checked;
    let formIsValid = bookingForm.checkValidity();
    let totalCost = 0;

    const totalCostCalc = () => {
        totalCost = isPlayer ? playerCostValue : monsterCostValue;

        if (isCatering) {
            totalCost += isPlayer ? playerCateringCostValue : monsterCateringCostValue;
        }
    }

    totalCostCalc()

    if (isPlayer) {
        characterNameInput.required = true;
        characterFactionInput.required = true;
    }

    const initPayPalButton = () => {
        if (formIsValid && !bookingForm['has_paid'].checked) {
            paypal.Buttons({
                style: {
                    shape: 'rect',
                    color: 'gold',
                    layout: 'vertical',
                    label: 'paypal',
                },

                createOrder: function (data, actions) {
                    const eventName = document.getElementById('event-name').innerText

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
                        bookingForm['has_paid'].checked = true;

                        // Full available details
                        console.log('Capture result', orderData);

                        // Show a success message within this page, e.g.
                        document.getElementById('paypal-button-container').innerHTML = '<h3>Thank you for your payment!</h3>';

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

        document.getElementById('paypal-button-container').innerHTML = ''

        fetch('/validate-booking/', {body: new FormData(bookingForm), method: 'POST'})
            .then(response => {
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
                        initPayPalButton();
                    } else {
                        document.getElementById('paypal-button-container').innerHTML =
                            '<input class="button is-link is-large is-fullwidth" type="submit" value="Submit">';
                    }
                } else {
                    document.getElementById('paypal-button-container').innerHTML =
                        '<div class="block has-background-light p-6"><p>Please ensure you have filled in all required fields in order to finish booking</p></div>';
                }
            })
            .catch(error => {
                formIsValid = false;
                console.error('ERROR - The following error occurred:', error)
                console.error('Please contact Jackals Faction staff with more details')
            }).finally(() => {
                if (bookingForm['has_paid'].checked) {
                    document.getElementById('paypal-button-container').innerHTML =
                            '<input class="button is-link is-large is-fullwidth" type="submit" value="Submit">';
                }
            })
    }

    const playerTypeSwitch = (type) => {
        switch (type) {
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
                characterNameInput.value = '';
                characterNameInput.required = false;
                characterFactionInput.value = '';
                characterFactionInput.required = false;
                break;
        }
    }

    const calculateCosts = () => {
        totalCostCalc()
        totalCostDisplay.innerText = (totalCost / 100).toFixed(2);
        validateForm();
    }

    bookingForm.addEventListener('change', (evt) => {
        if (evt.target.id === 'id_player_type') {
            playerTypeSwitch(evt.target.value)
        }

        if (evt.target.id === 'id_is_catering') {
            isCatering = !!evt.target.checked;
        }

        calculateCosts();
    })

    setTimeout(() => {
        playerTypeSwitch(document.getElementById('id_player_type').value);
        calculateCosts();
    }, 300)
})
