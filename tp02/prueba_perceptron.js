var input1 = new Bias (0, "P");
var input2 = new Bias (1, "Q");
var perceptron = new Perceptron ([input1, input2]);

function entrenamiento_conjunto (casos) {
	var aprendiendo = false;
	casos.forEach ((caso) => {
		var valor1 = caso[0];
		var valor2 = caso[1];
		var resultado_esperado = caso[2];

		input1.set (valor1);
		input2.set (valor2);
		var nuevo_aprendizaje = perceptron.entrenar (resultado_esperado);
		aprendiendo = (aprendiendo || nuevo_aprendizaje);
	});
	return aprendiendo;
}

function entrenamiento_intensivo (casos) {
	var iteraciones = 0;
	while (entrenamiento_conjunto (casos)) {
		console.log ("Perceptron esta aprendiendo");
		iteraciones++;
	}
	console.log ("Perceptron aprendio despues de "+ iteraciones +" iteraciones");
}


var conjunto_entrenamiento = [
	[0, 0, 0],
	[0, 1, 0],
	[1, 0, 0],
	[1, 1, 1]
];

console.log ("");
console.log ("ESTADO INCIAL DEL PERCEPTRON");
perceptron.imprimir_pesos ();
console.log ("");
console.log ("ENTRENAR PERCEPTRON");
entrenamiento_intensivo (conjunto_entrenamiento);
console.log ("");
console.log ("ESTADO FINAL DEL PERCEPTRON");
perceptron.imprimir_pesos ();

