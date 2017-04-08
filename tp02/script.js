var input1 = new Bias (0, "P");
var input2 = new Bias (1, "Q");
var perceptron = new Perceptron ([input1, input2]);
var ESPERA_ENTRENAMIENTO = 100;

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
		actualizar_vista ();
	});
	return aprendiendo;
}

function entrenamiento_intensivo (casos, iteracion=1) {
	document.querySelector ("#label_estado").textContent = "Aprendiendo... ("+iteracion+")";
	if (entrenamiento_conjunto (casos)) {
		console.log ("Perceptron esta aprendiendo");
		temporizador_entrenamiento = window.setTimeout (function () {
			entrenamiento_intensivo (casos, iteracion+1)
		}, ESPERA_ENTRENAMIENTO);
	} else {
		console.log ("Perceptron aprendio despues de "+ iteracion +" iteraciones");
		document.querySelector ("#label_estado").textContent = "Perceptron aprendio despues de "+ iteracion +" iteraciones";
		detener_entrenamiento();
	}
}

 var presets = {
	"p": [
		[0, 0, 0],
		[0, 1, 0],
		[1, 0, 1],
		[1, 1, 1]
	],
	"q": [
		[0, 0, 0],
		[0, 1, 1],
		[1, 0, 0],
		[1, 1, 1]
	],
	"and": [
		[0, 0, 0],
		[0, 1, 0],
		[1, 0, 0],
		[1, 1, 1]
	],
	"or": [
		[0, 0, 0],
		[0, 1, 1],
		[1, 0, 1],
		[1, 1, 1]
	],
	"xor": [
		[0, 0, 0],
		[0, 1, 1],
		[1, 0, 1],
		[1, 1, 0]
	],
	"np": [
		[0, 0, 1],
		[0, 1, 1],
		[1, 0, 0],
		[1, 1, 0]
	],
	"nq": [
		[0, 0, 1],
		[0, 1, 0],
		[1, 0, 1],
		[1, 1, 0]
	],
	"nand": [
		[0, 0, 1],
		[0, 1, 1],
		[1, 0, 1],
		[1, 1, 0]
	],
	"nor": [
		[0, 0, 1],
		[0, 1, 0],
		[1, 0, 0],
		[1, 1, 0]
	]
}

function entrenar () {
	var conjunto_entrenamiento = get_matriz_entrenamiento ();	
	document.querySelector ("button#button_entrenar").disabled = true;
	document.querySelector ("button#button_detener").style.display="block";
	console.log ("");
	console.log ("ESTADO INCIAL DEL PERCEPTRON");
	perceptron.imprimir_pesos ();
	console.log ("");
	console.log ("ENTRENAR PERCEPTRON");
	entrenamiento_intensivo (conjunto_entrenamiento);
	console.log ("");
	console.log ("ESTADO FINAL DEL PERCEPTRON");
	perceptron.imprimir_pesos ();
}

function detener_entrenamiento() {
	document.querySelector ("button#button_entrenar").disabled = false;
	document.querySelector ("button#button_detener").style.display="none";
	window.clearTimeout (temporizador_entrenamiento);
}

function get_matriz_entrenamiento () {
	var tbody = document.querySelector ("table.conjunto_entrenamiento tbody");
	var trs = tbody.children;
	var casos = [];
	for (var n_caso=0; n_caso< trs.length; n_caso++) {
		var caso = [];
		var tr = trs [n_caso];
		var tds = tr.children;
		for (var n_td=0; n_td < tds.length; n_td++) {
			var td = tds[n_td];
			var input = td.firstChild;
			caso.push (input.value);
		}
		casos.push (caso);
	}
	return casos;
}

function on_preset_changed () {
	var selected = document.querySelector ("select[name=preset]").value;
	if (selected == "custom") {
		var inputs = document.querySelectorAll ("table.conjunto_entrenamiento input");
		for (var i=0; i<inputs.length; i++) {
			inputs[i].disabled = false;
		}
	} else {
		var conjunto_entrenamiento = presets[selected];
		for (var n_caso = 0; n_caso < conjunto_entrenamiento.length; n_caso++) {
			var caso = conjunto_entrenamiento[n_caso];
			for (var n_dato = 0; n_dato < caso.length; n_dato++) {
				var dato = caso[n_dato];
				var input = document.querySelector ("table.conjunto_entrenamiento tr:nth-child("+(n_caso+1)+") td:nth-child("+(n_dato+1)+") input");
				input.value = dato;
				input.disabled = true;
			}
		}
		var inputs = document.querySelectorAll ("table.conjunto_entrenamiento input");
		for (var i=0; i<inputs.length; i++) {
			inputs[i].disabled = true;
		}
	}
}

function on_train_pressed () {
	entrenar ();
}

function on_stop_pressed () {
	detener_entrenamiento ();
}



function actualizar_vista () {
	var peso_p, peso_q, peso_bias;
	perceptron.pesos.forEach ((peso, obj) => {
		switch (obj.name) {
			case "P": peso_p = peso; break;
			case "Q": peso_q = peso; break;
			case "Bias": peso_bias = peso; break;
		}
	});
	document.querySelector ("dd#dd_p").textContent = peso_p;
	document.querySelector ("dd#dd_q").textContent = peso_q;
	document.querySelector ("dd#dd_bias").textContent = peso_bias;
}

window.onload = function () {
	on_preset_changed ();
	actualizar_vista ();
}
