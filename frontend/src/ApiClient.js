const API_URL = "http://localhost:8081";

export function getProblemInstance() {
    return fetch(`${API_URL}/problem`)
        .then(res => res.json());
}

export function postGuess(correctLocation, guessedLocation) {
    return fetch(`${API_URL}/guess`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            correct_location: correctLocation,
            guessed_location: guessedLocation,
        })
    }).then(res => res.json());
}
