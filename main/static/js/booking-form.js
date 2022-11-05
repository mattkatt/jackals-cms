const PLAYER = 'PL'
const MONSTER = 'MN'

function show(element) {
    if (Array.isArray(element)) {
        element.forEach(elm => {show(elm)})
    } else {
        element.classList.remove('is-hidden')
    }
}

function hide(element) {
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

    characterNameInput.required = true;
    characterFactionInput.required = true;

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
    })
})
