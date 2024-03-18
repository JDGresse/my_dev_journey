/* Setting variables with let function
let age = 25;
let year = 2024;

// Log/Print to console
console.log(age, year);

// Change var age value
age = 30;
console.log(age);

// Using const to create a variable (newer way)
const points = 100;
// points = 50; 
// -> if this is uncommented, we get an error, beacuse points is set to const 
console.log(points); */

/* Can also use var to set a variable (old way)
var score = 75;
console.log(score);


// Strings
console.log('hello world');

let email = 'email@example.com';
console.log(email);

// String concatenation
let firtsName = 'John';
let lastName = 'Doe';

let fullName = firtsName + ' ' + lastName
console.log(fullName);

// Getting characters
console.log(fullName[0]);
console.log(fullName[5]);

// String length
console.log(fullName.length);

// String methods -> do not alter original value we created
console.log(fullName.toUpperCase());
let result = fullName.toLocaleLowerCase(); 
console.log(result);

let index = email.indexOf('@'); // -> '@' refered to as argument
console.log(index); */

/* Common String methods
let email = 'email@example.com';

// let result = email.lastIndexOf('e');
// let result = email.slice(4,7);
// let result = email.substring(4, 16);
// let result = email.replace('.', 's.') -> replace the first one it comes across

console.log(result); */

// Template String or Template literals
const title = 'Best of 2024';
const author = 'John';
const recommended = 300;

// Concatenation
//let result = title + ' ' + author + ' ' + recommended;

// Template string (similar to f strings)
//let result = `The blog called ${title} by ${author} has ${recommended} recommendeds.`;

/* Create HTML Template
let html = `
    <h2>${title}</h2>
    <p>By ${author}<p>
    <span>has ${recommended} recommendeds</span>`;

console.log(html); */

/*  truthy values 
        -> all vaues except 0
        -> string of any length

    falsy values
        -> 0
        -> string of length = 0
*/


