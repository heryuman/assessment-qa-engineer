## Resumen de hallazgos y Listado de Bugs


* Bug que no permite obtener la suma del total de inventario: [Bug01](https://github.com/heryuman/assessment-qa-engineer/issues/1)
* Bug que no permite visualizar los productosque estan debajo del stock [Bug02](https://github.com/heryuman/assessment-qa-engineer/issues/2)
* Bug que devuelve erro en el servidor al ingresar un costo cero al calcualr margen de ganancia [Bug03](https://github.com/heryuman/assessment-qa-engineer/issues/3)
* Bug que no muestra codigo http ni mensaje de error al vencer el token de acceso [Bug04](https://github.com/heryuman/assessment-qa-engineer/issues/4)


## Recomendaciones de Mejora
* Es necesario considerar ciertas validaciones sobre valores que el usuario pueda ingresar
* Evitar dejar valores (SECRETS KEYS) quemados en el código para evitar filtraciones de datos sensibles de usuario


## Pasos para ejecutar pruebas
Ejecutar el comando en la raiz del proyecto
```bash
$ pytest --cov=main --cov-branch --cov-report=html --cov-report=term-missing --html=report.html --self-contained-html
```