let a = 10;
let b = 20;
let c = a + b * 2;
print("C is:");
print(c);
if (c == 50) {
    print("Success: c is 50");
} else {
    print("Failure: c is not 50");
}

let neg = -c;
print("Negated:");
print(neg);

let m = [[1, 2], [3, 4]];
print("Matrix m:");
print(m);
print("Transposed m:");
print(m.Transpose());
print("Is m invertible?");
print(m.isInvertible());

let s = [[1, 2], [2, 4]];
print("Does s have a null space?");
print(s.hasNull());
print("Reduced s:");
print(s.Reduce());

let greeting = "Hello, " + "MyLang";
print(greeting);
