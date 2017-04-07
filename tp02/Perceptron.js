class Bias {
	constructor (value, name) {
		this.value = value
		this.name = name;
	}

	set (value) {
		this.value = value
	}

	get () {
		return this.value;
	}
}

class Perceptron {
	constructor (entradas) {
		this.factor_aprendizaje = 1;
		this.entradas = entradas;
		this.entradas.push (new Bias (1, "Bias"));
		this.pesos = new Map ();
		this.entradas.forEach ((entrada) => this.pesos.set (entrada, 1-2*Math.random()));
		//this.entradas.forEach ((entrada) => this.pesos.set (entrada, 0));
	}

	get () {
		var sum = 0;
		this.entradas.forEach ((entrada) => sum += entrada.get() *this.pesos.get(entrada));
		return this.escalon (sum);
	}

	entrenar (resultado_esperado) {
		var sum = 0;
		var entradas_leidas = new Map ();
		var str_entradas = "";
		this.entradas.forEach ((entrada) => {
			var leido = entrada.get ();
			sum += leido * this.pesos.get (entrada);
			entradas_leidas.set (entrada, leido)
			str_entradas += leido + " ";
		});
		var resultado_obtenido = this.escalon (sum);
		var aprendiendo = (resultado_obtenido != resultado_esperado);
		if (aprendiendo) {
			this.actualizar_pesos (entradas_leidas, resultado_obtenido, resultado_esperado);
		}
		console.log (" [" + str_entradas + "] -> " + resultado_obtenido + (aprendiendo ? " WRONG": " OK"));
		return aprendiendo;
	}

	actualizar_pesos (entradas_leidas, resultado_obtenido, resultado_esperado) {
		var diferencia = resultado_esperado - resultado_obtenido;
		this.entradas.forEach ((entrada) => {
			var leido = entradas_leidas.get (entrada);
			var peso_actual = this.pesos.get (entrada);
			var peso_nuevo = peso_actual + (this.factor_aprendizaje * diferencia * leido);
			this.pesos.set (entrada, peso_nuevo);
		});
	}

	escalon (num) {
		if (num > 0) {
			return 1;
		} else {
			return 0;
		}
	}
	
	imprimir_pesos () {
		var num_entrada=1;
		console.log ("Pesos sinapticos:");
		this.pesos.forEach ((valor, clave, map) => {
			console.log (" " + clave.name + ": "+ valor);
			num_entrada++;
		});
	}
}

