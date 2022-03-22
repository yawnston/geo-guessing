export function getProblemInstance() {
    return fetch("http://localhost:8081/problem")
        .then(res => res.json());
}
