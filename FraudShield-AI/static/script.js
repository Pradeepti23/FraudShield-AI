// ======================================================
// FRAUDSHIELD-AI
// CLIENT SIDE VALIDATION
// ======================================================

document.addEventListener("DOMContentLoaded", () => {

    const form = document.querySelector("form");

    if (!form) return;

    form.addEventListener("submit", (e) => {

        // ==========================================
        // GET INPUTS
        // ==========================================
        const amount = document.querySelector(
            "[name='transaction_amount']"
        );

        const age = document.querySelector(
            "[name='customer_age']"
        );

        const transactions = document.querySelector(
            "[name='transactions_today']"
        );

        const button = form.querySelector("button");


        // ==========================================
        // RESET BORDERS
        // ==========================================
        amount.style.border = "";
        age.style.border = "";
        transactions.style.border = "";


        // ==========================================
        // READ VALUES
        // ==========================================
        const amountVal = parseFloat(amount.value);

        const ageVal = parseInt(age.value);

        const transactionVal = parseInt(transactions.value);


        // ==========================================
        // AMOUNT VALIDATION
        // ==========================================
        if (isNaN(amountVal) || amountVal <= 0) {

            amount.style.border = "2px solid red";

            alert(
                "Transaction amount must be greater than zero."
            );

            e.preventDefault();

            return;
        }


        // ==========================================
        // AGE VALIDATION
        // ==========================================
        if (isNaN(ageVal) || ageVal < 18 || ageVal > 100) {

            age.style.border = "2px solid red";

            alert(
                "Customer age must be between 18 and 100."
            );

            e.preventDefault();

            return;
        }


        // ==========================================
        // TRANSACTION COUNT VALIDATION
        // ==========================================
        if (isNaN(transactionVal) || transactionVal < 0) {

            transactions.style.border = "2px solid red";

            alert(
                "Transactions today cannot be negative."
            );

            e.preventDefault();

            return;
        }


        // ==========================================
        // LOADING STATE
        // ==========================================
        if (button) {

            button.disabled = true;

            button.innerHTML = `
                ⏳ Predicting...
            `;

        }

    });

});