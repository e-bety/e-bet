document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("game-form");
    const numberSelection = document.getElementById("number-selection");
    const resultDiv = document.getElementById("result");

    // Générer 5 lots de 2 sélections de nombres
    function createNumberInputs() {
        for (let i = 0; i < 5; i++) {
            const div = document.createElement("div");
            div.innerHTML = `
                <label>Lot ${i + 1} :</label>
                <input type="number" class="num-input" min="1" max="99" required>
                <input type="number" class="num-input" min="1" max="99" required>
            `;
            numberSelection.appendChild(div);
        }
    }

    createNumberInputs();  // Création des champs à l'ouverture de la page

    form.addEventListener("submit", async function (event) {
        event.preventDefault();

        const username = document.getElementById("username").value;
        const bet = parseFloat(document.getElementById("bet").value);
        const numInputs = document.querySelectorAll(".num-input");

        let userNumbers = [];
        for (let i = 0; i < numInputs.length; i += 2) {
            let num1 = parseInt(numInputs[i].value);
            let num2 = parseInt(numInputs[i + 1].value);
            if (!num1 || !num2 || num1 === num2 || num1 < 1 || num1 > 99 || num2 < 1 || num2 > 99) {
                alert("Veuillez entrer des numéros valides entre 1 et 99.");
                return;
            }
            userNumbers.push([num1, num2]);
        }

        // Envoi des données au backend
        const response = await fetch("/play", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, numbers: userNumbers, bet })
        });

        const result = await response.json();
        if (result.error) {
            resultDiv.innerHTML = `<p style="color: red;">${result.error}</p>`;
            return;
        }

        // Affichage des résultats
        resultDiv.innerHTML = `
            <p><strong>Numéros générés (Lot 1) :</strong> ${JSON.stringify(result.generated_lot_1)}</p>
            <p><strong>Numéros générés (Lot 2) :</strong> ${JSON.stringify(result.generated_lot_2)}</p>
            <p><strong>Vos lots :</strong> ${JSON.stringify(result.user_lots)}</p>
            <p><strong>Mise :</strong> ${result.bet} f par lot</p>
            <p><strong>Gain total :</strong> ${result.total_winnings} f</p>
            <p><strong>Nouveau solde :</strong> ${result.new_balance} f</p>
        `;
    });
});
