// Function declaration
function greet() {
    console.log('Hello');
}

// Function call/ invoke
greet();

// Function expression
const speak = function() {
    console.log('World');
};

speak();

// -> hoisting --> function declarations get hoisted to the top of the stack, but not with function expressions
// ---> this means that functions can be called before declaring of the funstion

// const calcArea = function(radius) {
//     return 3.14 * radius**2;
// };


// Arrow functions format
// const calcArea = (radius) =>{
//     return 3.14 * radius**2;
// };

// For only 1x variable
// const calcArea = radius =>{
//     return 3.14 * radius**2;
// };

// For only return statement
const calcArea = radius => 3.14 * radius**2;

const area = calcArea(5);
console.log('Area: ', area);


