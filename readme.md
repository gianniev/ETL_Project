# Proyecto Final 
### ETL Cryptomonedas. Coinmarketcap

##### El proyecto consiste en extraer de la API de [CoinMarketcap](htpps://Coinmarketcap.com) información relevante de por lo menos 2000 criptomonedas diferentes, y luego se crea una tabla en Amazon Redshift y se ingestan los datos extraidos de la API. Al finalizar la tarea se envia un correo electrónico confirmando la ingesta de los datos en la tabla.
---

1. Para comenzar el proyecto hay que crear las carpetas necesarias con el comando bash: 

```bash
mkdir -p ./{logs,dags,config,plugins}
```
2. Para iniciar Airflow en un entorno docker se utiliza el siguiente comando bash:
```bash
docker-compose up airflow-init
```
3. Para iniciar y ejecutar todos los servicios definidos en docker-compose.yaml inciamos el comando:
```bash
docker-compose up
```
*El puerto de la interface de Airflow es 8081. Desde mi PC, cuando la interface está lista me da error '404 page not found' al ingresar al link, pero al volver a intentar se abre correctamente. Me pasa lo mismo luego de iniciar sesión, hay un error '404 page not found', pero al re abrir el link del puerto se entra correctamente. Aveces cuando se inicia el DAG desde Airflow también me da un error la interface, pero al re abrir la página todo se ejecuta correctamente. Yo creo que esto es un error de la interface de Airflow ya que en realidad todo funciona correctamente.*

4. Para configurar el receptor del email que será enviado al finalizar el script, hay que ingresar a docker-compose.yaml y modificar la variable 
'AIRFLOW_VAR_TO_ADDRESS'. Para enviar 1 correo solo dejar el correo entre comas ejemplo ('pablo@gmail.com'). Para agregar dos correos poner una coma y un espacio. Ejemplo ('pablo@gmail.com, juan@gmail.com')

```yaml
AIRFLOW_VAR_TO_ADDRESS: 'gianni.ev93@gmail.com, daniel.indra92@gmail.com'
```

*Revisar carpeta de spam. A mi me llegaban los correos a la carpeta de spam. Tuve que desbloquear al emisor, en este caso 'gianni.coder.space@gmail.com'.*
