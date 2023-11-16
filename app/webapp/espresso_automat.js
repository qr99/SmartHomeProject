const form = document.getElementById("myForm");
const loadingBar = document.getElementById("loading-bar");
const output = document.getElementById("output");
const submitButton = document.getElementById("submitButton");
const API_URL_PREFIX = "api/1.0/";


async function triggerBehaviourTree(program, temperature, strength, quantity) {
    var coffee_machine_parameters = {};
    await $.ajax({
        type: "POST",
        url: API_URL_PREFIX  + "trigger_espresso_automat_tree/",
        contentType: "application/json",
        data: JSON.stringify({
            program: program,
            temperature: temperature,
            strength: strength,
            quantity: quantity
        }),
        success: function (response) {
            coffee_machine_parameters = response;
        },
        error: function (error) {
            console.log("error: " + error)
        },
    });
    return coffee_machine_parameters;
};

form.addEventListener("submit", async function(event) {
    event.preventDefault(); // Prevent the default form submission

    const program = document.getElementById("program").value;
    const temperature = document.getElementById("temperature").value;
    const strength = document.getElementById("strength").value;
    const quantity = document.getElementById("quantity").value;

    loadingBar.style.display = "block"; // Display the loading bar
    output.style.display = "block"; // Display the output
    submitButton.disabled = true; // Disable the submit button

    var behavior_tree_response = await triggerBehaviourTree(program, temperature, strength, quantity);

    output.innerHTML = "<ul><li>Program: " + behavior_tree_response['program'] +
        "</li><li>Temperature: " + behavior_tree_response['temperature'] +
        "</li><li>Strength: " + behavior_tree_response['strength'] +
        "</li><li>Quantity: " + String(behavior_tree_response['quantity']) + "</li></ul>";

    // Simulate a delay for the loading effect (you can replace this with your actual form submission logic)
    setTimeout(function() {
        loadingBar.style.display = "none"; // Hide the loading bar
        output.style.display = "none"; // Hide the output
        submitButton.disabled = false; // Enable the submit button
    }, 4000); // Replace 4000 with the time your form submission takes in milliseconds
});