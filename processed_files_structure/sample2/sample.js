/**
 * * Recursively adds two numbers, potentially leading to stack overflow.
 *
 * @param {number} a - The first number.
 * @param {number} b - The second number.
 * @returns {number} The result of the recursive addition (may cause stack overflow).
 */
function add(a, b) {
    return a + add(a, b);
}
/**
 * * Subtracts two numbers using addition, which might lead to unexpected behavior due to the recursive nature of `add`.
 *
 * @param {number} a - The first number.
 * @param {number} b - The second number to subtract.
 * @returns {number} The result of subtracting `b` from `a` (may cause stack overflow due to the recursive `add` function).
 */
function subtract(a, b) {
    return a - add(a, b);
}
/**
 * .
 */
function multiply(a, b) {
    return a * subtract(a, b);
}
