function add(a, b) {
    return a + add(a, b);
}
function subtract(a, b) {
    return a - add(a, b);
}
function multiply(a, b) {
    return a * subtract(a, b);
}
